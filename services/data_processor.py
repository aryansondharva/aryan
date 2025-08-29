# services/data_processor.py
from typing import Dict, Any, List, Optional
import io
import logging
from pathlib import Path

# Try to import optional dependencies
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas not installed. CSV/Excel processing will be limited.")

try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("Warning: pdfplumber not installed. PDF processing will be disabled.")

logger = logging.getLogger(__name__)

class DataProcessor:
    """Handles file processing and data analysis for CSV and PDF files."""
    
    def __init__(self):
        self.current_data = None
        self.file_info = {}
    
    def process_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process uploaded file and return analysis results."""
        try:
            file_extension = Path(filename).suffix.lower()
            
            # Store filename for context
            self.file_info['filename'] = filename
            
            if file_extension == '.csv':
                if not PANDAS_AVAILABLE:
                    raise ValueError("pandas is required for CSV processing. Please install: pip install pandas")
                return self._process_csv(file_content, filename)
            elif file_extension == '.pdf':
                if not PDF_AVAILABLE:
                    raise ValueError("pdfplumber is required for PDF processing. Please install: pip install pdfplumber")
                return self._process_pdf(file_content, filename)
            elif file_extension in ['.xlsx', '.xls']:
                if not PANDAS_AVAILABLE:
                    raise ValueError("pandas and openpyxl are required for Excel processing. Please install: pip install pandas openpyxl")
                return self._process_excel(file_content, filename)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
                
        except Exception as e:
            logger.error(f"Error processing file {filename}: {e}")
            return {
                "success": False,
                "error": str(e),
                "filename": filename
            }
    
    def _process_csv(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process CSV file and extract insights."""
        if not PANDAS_AVAILABLE:
            raise Exception("pandas is required for CSV processing")
        try:
            # Read CSV
            df = pd.read_csv(io.BytesIO(file_content))
            self.current_data = df
            
            # Basic analysis
            analysis = self._analyze_dataframe(df, filename)
            
            return {
                "success": True,
                "file_type": "CSV",
                "filename": filename,
                "analysis": analysis,
                "preview": df.head(5).to_dict('records'),
                "columns": list(df.columns),
                "shape": df.shape
            }
            
        except Exception as e:
            raise Exception(f"Failed to process CSV: {str(e)}")
    
    def _process_excel(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process Excel file and extract insights."""
        if not PANDAS_AVAILABLE:
            raise Exception("pandas and openpyxl are required for Excel processing")
        try:
            # Read Excel
            df = pd.read_excel(io.BytesIO(file_content))
            self.current_data = df
            
            # Basic analysis
            analysis = self._analyze_dataframe(df, filename)
            
            return {
                "success": True,
                "file_type": "Excel",
                "filename": filename,
                "analysis": analysis,
                "preview": df.head(5).to_dict('records'),
                "columns": list(df.columns),
                "shape": df.shape
            }
            
        except Exception as e:
            raise Exception(f"Failed to process Excel: {str(e)}")
    
    def _process_pdf(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process PDF file and extract text/tables."""
        if not PDF_AVAILABLE:
            raise Exception("pdfplumber is required for PDF processing")
        try:
            text_content = []
            tables = []
            
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(f"Page {page_num}:\n{page_text}")
                    
                    # Extract tables
                    page_tables = page.extract_tables()
                    if page_tables:
                        for table_num, table in enumerate(page_tables, 1):
                            if table:
                                # Convert table to DataFrame for analysis
                                df = pd.DataFrame(table[1:], columns=table[0])
                                tables.append({
                                    "page": page_num,
                                    "table": table_num,
                                    "data": df.to_dict('records'),
                                    "columns": list(df.columns)
                                })
            
            # Combine all text
            full_text = "\n\n".join(text_content)
            
            # Basic analysis
            analysis = {
                "total_pages": len(pdf.pages),
                "total_text_length": len(full_text),
                "tables_found": len(tables),
                "key_insights": self._extract_pdf_insights(full_text, tables)
            }
            
            return {
                "success": True,
                "file_type": "PDF",
                "filename": filename,
                "analysis": analysis,
                "text_content": full_text[:2000] + "..." if len(full_text) > 2000 else full_text,
                "tables": tables[:3],  # Limit to first 3 tables
                "full_text": full_text
            }
            
        except Exception as e:
            raise Exception(f"Failed to process PDF: {str(e)}")
    
    def _analyze_dataframe(self, df: pd.DataFrame, filename: str) -> Dict[str, Any]:
        """Perform comprehensive analysis on DataFrame."""
        analysis = {
            "basic_info": {
                "rows": len(df),
                "columns": len(df.columns),
                "memory_usage": df.memory_usage(deep=True).sum(),
                "missing_values": df.isnull().sum().to_dict()
            },
            "column_types": df.dtypes.astype(str).to_dict(),
            "numeric_summary": {},
            "categorical_summary": {},
            "key_insights": []
        }
        
        # Numeric columns analysis
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            analysis["numeric_summary"] = df[numeric_cols].describe().to_dict()
            
            # Find trends and patterns
            for col in numeric_cols:
                if df[col].notna().sum() > 0:
                    mean_val = df[col].mean()
                    std_val = df[col].std()
                    min_val = df[col].min()
                    max_val = df[col].max()
                    
                    analysis["key_insights"].append(
                        f"{col}: Average {mean_val:.2f}, Range {min_val:.2f} to {max_val:.2f}"
                    )
        
        # Categorical columns analysis
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            for col in categorical_cols[:5]:  # Limit to first 5 categorical columns
                value_counts = df[col].value_counts().head(5).to_dict()
                analysis["categorical_summary"][col] = value_counts
                
                if len(value_counts) > 0:
                    top_value = list(value_counts.keys())[0]
                    top_count = list(value_counts.values())[0]
                    analysis["key_insights"].append(
                        f"{col}: Most common value is '{top_value}' ({top_count} occurrences)"
                    )
        
        return analysis
    
    def _extract_pdf_insights(self, text: str, tables: List[Dict]) -> List[str]:
        """Extract key insights from PDF content."""
        insights = []
        
        # Text-based insights
        if text:
            word_count = len(text.split())
            insights.append(f"Document contains {word_count} words")
            
            # Look for common business terms
            business_terms = ['revenue', 'sales', 'profit', 'growth', 'quarter', 'year', 'performance']
            found_terms = [term for term in business_terms if term.lower() in text.lower()]
            if found_terms:
                insights.append(f"Business-related content detected: {', '.join(found_terms)}")
        
        # Table-based insights
        if tables:
            insights.append(f"Found {len(tables)} data tables for analysis")
            
            for table in tables[:2]:  # Analyze first 2 tables
                if table['data']:
                    insights.append(f"Table on page {table['page']} has {len(table['data'])} rows")
        
        return insights
    
    def get_analysis_context(self) -> str:
        """Get current data context for LLM analysis."""
        if self.current_data is None:
            return "No data currently loaded. Please ask the user to upload a data file first."
        
        # Create a comprehensive summary of the current data
        if not PANDAS_AVAILABLE:
            return "Data analysis capabilities limited - pandas not available."
            
        df = self.current_data
        
        # Get basic statistics
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        context = f"""
CURRENT DATASET CONTEXT:
File loaded: {self.file_info.get('filename', 'Unknown')}
Shape: {df.shape[0]} rows, {df.shape[1]} columns
Columns: {', '.join(df.columns.tolist())}

NUMERIC COLUMNS: {', '.join(numeric_cols) if numeric_cols else 'None'}
CATEGORICAL COLUMNS: {', '.join(categorical_cols) if categorical_cols else 'None'}

SAMPLE DATA (first 5 rows):
{df.head(5).to_string()}

SUMMARY STATISTICS:
{df.describe().to_string() if len(numeric_cols) > 0 else 'No numeric data for statistics'}

KEY INSIGHTS AVAILABLE:
- You can analyze trends, patterns, and comparisons
- Data is ready for questions about performance, growth, regional analysis
- Ask specific questions about any column or metric shown above
"""
        
        return context
    
    def query_data(self, query: str) -> str:
        """Execute queries on the current dataset."""
        if self.current_data is None:
            return "No data loaded. Please upload a file first."
        
        try:
            df = self.current_data
            
            # Simple query processing (can be enhanced with NLP)
            query_lower = query.lower()
            
            if 'summary' in query_lower or 'describe' in query_lower:
                return df.describe().to_string()
            elif 'columns' in query_lower:
                return f"Columns: {', '.join(df.columns.tolist())}"
            elif 'shape' in query_lower or 'size' in query_lower:
                return f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns"
            elif 'missing' in query_lower or 'null' in query_lower:
                missing = df.isnull().sum()
                return f"Missing values:\n{missing.to_string()}"
            else:
                return "I can help you analyze the data. Try asking about summary, columns, shape, or missing values."
                
        except Exception as e:
            return f"Error querying data: {str(e)}"

# Global instance
data_processor = DataProcessor()

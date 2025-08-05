# Warehouse Management System (WMS)

A comprehensive Warehouse Management System developed for CSTE International assignment. This system provides SKU mapping, data processing, and inventory management capabilities.

## Features

### 1. SKU Mapping System
- **SKU to MSKU Mapping**: Automatically maps Stock Keeping Units (SKUs) to Master SKUs (MSKUs)
- **Combo Product Handling**: Supports products with multiple SKU components
- **Flexible Input Processing**: Handles various input formats for sales data

### 2. Data Processing
- **CSV/Excel Support**: Processes both CSV and Excel files
- **Data Cleaning**: Automatically cleans and validates uploaded data
- **Error Handling**: Robust error handling for missing mappings and invalid data

### 3. Web Application
- **Modern UI**: Clean, responsive web interface
- **Drag & Drop Upload**: Easy file upload functionality
- **Real-time Processing**: Immediate feedback on data processing status

### 4. Database Integration
- **PostgreSQL Support**: Relational database for data storage
- **Structured Schema**: Well-designed tables for SKUs, inventory, and sales data

## Project Structure

```
CSTE/
├── web_app/
│   ├── app.py                 # Main Flask application
│   ├── SKUMapper.py          # SKU mapping logic
│   └── templates/
│       └── index.html        # Web interface
├── database_setup.sql        # Database schema
├── setup_database.py         # Database initialization script
├── README.md                 # This file
└── data/                     # Sample data files
    ├── CSTE AMAZON/
    ├── CSTE FK/
    ├── GL FK/
    └── RUDRAV MEESHO/
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 17+
- pip (Python package manager)

### 1. Install Python Dependencies
```bash
pip install flask psycopg2-binary pandas openpyxl
```

### 2. Database Setup
```bash
# Run the database setup script
python setup_database.py
```

### 3. Start the Application
```bash
# Navigate to the web_app directory
cd web_app

# Start the Flask application
python app.py
```

### 4. Access the Application
Open your web browser and navigate to: `http://127.0.0.1:5000`

## Usage

### 1. Upload Data
- Click "Browse" or drag and drop CSV/Excel files
- Select multiple files if needed
- Click "Process Data" to start processing

### 2. Data Processing
- The system automatically maps SKUs to MSKUs
- Processes combo products correctly
- Validates and cleans the data

### 3. View Results
- Check the status message for processing results
- Review any errors or warnings

## Technical Implementation

### SKU Mapper Class
```python
class SKUMapper:
    def __init__(self, sku_data):
        self.sku_data = sku_data
        self.sku_to_msku = {}
    
    def map_sku(self, sku):
        return self.sku_to_msku.get(sku, None)
    
    def handle_combo(self, combo_sku):
        components = combo_sku.split('-')
        return [self.map_sku(sku) for sku in components]
```

### Database Schema
- **skus**: Stores SKU to MSKU mappings
- **inventory**: Tracks inventory quantities by SKU and warehouse
- **sales**: Records sales data by SKU and date

### Web Application Features
- **Flask Backend**: RESTful API for data processing
- **Modern Frontend**: Responsive HTML/CSS/JavaScript interface
- **File Upload**: Secure file handling with validation

## API Endpoints

- `GET /`: Main application interface
- `POST /upload`: Upload and process data files
- `GET /test-db`: Test database connection

## Data Formats Supported

### CSV Files
- Amazon sales data
- Flipkart order data
- Meesho order data
- Inventory data

### Excel Files
- WMS data sheets
- Combo product definitions
- SKU mapping tables

## Error Handling

- **Missing Files**: Clear error messages for missing uploads
- **Invalid Formats**: Validation for supported file types
- **Database Errors**: Graceful handling of connection issues
- **SKU Mapping**: Warnings for unmapped SKUs

## Future Enhancements

1. **Real-time Dashboard**: Live inventory and sales analytics
2. **Advanced Analytics**: Sales forecasting and trend analysis
3. **Multi-warehouse Support**: Handle multiple warehouse locations
4. **API Integration**: Connect with external marketplace APIs
5. **Mobile App**: Native mobile application for field operations

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Ensure PostgreSQL is running
   - Check database credentials in `app.py`
   - Verify port configuration (default: 5432)

2. **File Upload Errors**
   - Check file format (CSV/Excel only)
   - Ensure file size is reasonable
   - Verify file permissions

3. **SKU Mapping Issues**
   - Review SKU data in `SKUMapper.py`
   - Check for typos in SKU names
   - Verify combo product definitions

## Support

For technical support or questions about the implementation, please refer to the code comments and this documentation.

## License

This project is developed for CSTE International assignment purposes. 
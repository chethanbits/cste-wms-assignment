from flask import Flask, request, jsonify, render_template
import psycopg2
import pandas as pd
import os
from SKUMapper import SKUMapper
from datetime import datetime

app = Flask(__name__)

# Initialize SKUMapper with sample data
sku_data = {
    'pen': 'cste-pen',
    'pen-blue': 'cste-pen',
    'pen-blue2': 'cste-pen-black'
}
mapper = SKUMapper(sku_data)
mapper.load_mappings()

# Store processed results temporarily
processed_results = []

# Database connection parameters
DB_PARAMS = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'your_password_here'  # Replace with your actual PostgreSQL password
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

def save_to_database(file_data, processed_data):
    """Save processed data to PostgreSQL database"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        create_tables_sql = """
        CREATE TABLE IF NOT EXISTS processed_files (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            total_rows INTEGER NOT NULL,
            columns_count INTEGER NOT NULL,
            processed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS sku_mappings (
            id SERIAL PRIMARY KEY,
            file_id INTEGER REFERENCES processed_files(id),
            original_sku VARCHAR(255) NOT NULL,
            mapped_msku VARCHAR(255),
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_tables_sql)
        
        # Insert file information
        cursor.execute("""
            INSERT INTO processed_files (filename, total_rows, columns_count)
            VALUES (%s, %s, %s) RETURNING id
        """, (file_data['filename'], file_data['total_rows'], file_data['columns_count']))
        
        file_id = cursor.fetchone()[0]
        
        # Insert SKU mappings
        for item in processed_data:
            original_sku = item.get('SKU') or item.get('FNSKU') or item.get('MSKU') or 'N/A'
            mapped_msku = item.get('MSKU') or item.get('FNSKU_MSKU') or item.get('MSKU_MSKU') or 'Not Mapped'
            
            cursor.execute("""
                INSERT INTO sku_mappings (file_id, original_sku, mapped_msku)
                VALUES (%s, %s, %s)
            """, (file_id, original_sku, mapped_msku))
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Database save error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_data():
    try:
        files = request.files.getlist('file')
        if not files:
            return jsonify({"error": "No files provided"}), 400
        
        processed_files = []
        file_results = []
        
        for file in files:
            if file.filename:
                # Read CSV file
                if file.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.filename.endswith('.xlsx'):
                    df = pd.read_excel(file)
                else:
                    continue
                
                # Process the data using SKU mapper
                processed_data = []
                if 'SKU' in df.columns:
                    df['MSKU'] = df['SKU'].apply(lambda x: mapper.map_sku(str(x)))
                    # Store first 5 rows as sample results
                    sample_data = df.head(5)[['SKU', 'MSKU']].to_dict('records')
                    processed_data.extend(sample_data)
                
                # Also check for other SKU-related columns
                sku_columns = [col for col in df.columns if 'sku' in col.lower() or 'SKU' in col]
                for sku_col in sku_columns:
                    if sku_col != 'SKU':  # Avoid duplicate processing
                        df[f'{sku_col}_MSKU'] = df[sku_col].apply(lambda x: mapper.map_sku(str(x)))
                        sample_data = df.head(3)[[sku_col, f'{sku_col}_MSKU']].to_dict('records')
                        processed_data.extend(sample_data)
                
                file_data = {
                    'filename': file.filename,
                    'total_rows': len(df),
                    'columns_count': len(df.columns),
                    'columns': list(df.columns),
                    'processed_data': processed_data
                }
                
                # Try to save to database
                db_saved = save_to_database(file_data, processed_data)
                file_data['db_saved'] = db_saved
                
                file_results.append(file_data)
                processed_files.append(file.filename)
        
        # Store results globally
        global processed_results
        processed_results = file_results
        
        return jsonify({
            "message": f"Successfully processed {len(processed_files)} files: {', '.join(processed_files)}",
            "results": file_results
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/results')
def show_results():
    return render_template('results.html', results=processed_results)

@app.route('/database-status')
def database_status():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM processed_files")
            files_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM sku_mappings")
            mappings_count = cursor.fetchone()[0]
            conn.close()
            return jsonify({
                "status": "connected",
                "files_processed": files_count,
                "sku_mappings": mappings_count
            })
        except:
            conn.close()
            return jsonify({"status": "tables_not_created"})
    else:
        return jsonify({"status": "not_connected"})

@app.route('/test-db')
def test_db():
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({"message": "Database connection successful!"})
    else:
        return jsonify({"error": "Database connection failed!"}), 500

if __name__ == '__main__':
    app.run(debug=True)
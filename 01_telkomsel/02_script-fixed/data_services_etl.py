import arcpy
import os

def extract_data_csv(input_data_csv, output_shp) :
    if not os.path.exists(output_shp):
        os.makedirs(output_shp)

    data_ = arcpy.ListTables("*.csv")

    for table in data_:
        # Membuat path lengkap untuk tabel
        table_path = os.path.join(input_data_csv, table)

        # Membaca daftar nama kolom dalam tabel
        table_fields = [field.name for field in arcpy.ListFields(table_path)]

        # Memeriksa apakah kolom "Longitude" dan "Latitude" ada dalam tabel
        if "Longitude" in table_fields and "Latitude" in table_fields:
            # Membuat nama output dari nama tabel
            output_name = os.path.splitext(table)[0] + ".shp"

            # Membuat path lengkap untuk output
            output_path = os.path.join(output_shp, output_name)
            
            try :
                # Mengekstrak tabel CSV ke feature class
                arcpy.management.XYTableToPoint(table_path, output_path, "Longitude", "Latitude")

                print(f"Ekstraksi selesai: {table_path} -> {output_path}")
            except arcpy.ExecuteError :
                print(f"Data tidak dapat diekstrak : {table_path}")
        else:
            print(f"Kolom 'Longitude' atau 'Latitude' tidak ditemukan dalam tabel: {table_path}")

#Function yang digunakan hanya untuk mengidentifikasi object 
def clean_filename(filename):
    # Menghapus karakter "()"
    clean_name = filename.replace('(', '').replace(')', '').replace(' ', '_').replace('`', '').replace("'", '')
    # Mengganti spasi dengan "_"
    # clean_name = clean_name.replace(' ', '_') # semua object dianggap pengacau digabung langsung saja
    return clean_name

def clean_and_rename_files(input_folder):
    
    files = os.listdir(input_folder)
    
    rename_operations = []
    
    # Process each file in the input folder
    for file in files:
        input_path = os.path.join(input_folder, file)

        # Skip directories
        if os.path.isdir(input_path):
            continue

        cleaned_name = clean_filename(file)
        output_path = os.path.join(input_folder, cleaned_name)

        # Check if the cleaned filename is different from the original filename
        if cleaned_name != file:
            # Rename the file
            rename_operations.append((input_path, output_path))
        else:
            print(f"File {file} is already correctly named. No changes were made.")
            
    for input_path, out in rename_operations :
        os.rename(input_path, output_path)
        print(f"Renamed {os.path.basename(input_path)} to {os.path.basename(output_path)}.")

# Example usage:
input_folder = '/path/to/your/input/folder'
clean_and_rename_files(input_folder)

            


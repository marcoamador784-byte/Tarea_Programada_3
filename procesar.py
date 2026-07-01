import os
from PIL import Image
import xlsxwriter

def procesar_imagenes():
    """
    Realiza el procesamiento por lotes de imágenes y genera un reporte en Excel.

    Esta función busca imágenes en formato JPG, JPEG o PNG dentro de la carpeta 
    'imagenes_entrada', verifica la existencia de una marca de agua, redimensiona 
    las imágenes a un tamaño máximo de 800x800 píxeles, las convierte a escala 
    de grises, les aplica la marca de agua en la esquina inferior derecha y las 
    guarda en 'imagenes_salida'. Además, registra los metadatos originales de 
    cada imagen procesada en un libro de Excel.

    :raises FileNotFoundError: Si no se encuentra el archivo de la marca de agua.
    :return: None
    """
    ruta_entrada = "imagenes_entrada"
    ruta_salida = "imagenes_salida"
    ruta_marca = "marca_agua.png"
    reporte_excel = "reporte_imagenes.xlsx"
    
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)
        
    if not os.path.exists(ruta_marca):
        print(f"Error: No se encontró la marca de agua en '{ruta_marca}'.")
        return

    img_marca = Image.open(ruta_marca)

    workbook = xlsxwriter.Workbook(reporte_excel)
    worksheet = workbook.add_worksheet("Inventario de Imágenes")
    
    formato_header = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
    formato_celda = workbook.add_format({'border': 1})
    
    headers = ["Nombre del archivo original", "Formato de la imagen", "Ancho original", "Alto original", "Estado"]
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, formato_header)
    
    fila_excel = 1
    formatos_soportados = (".jpg", ".jpeg", ".png")
    archivos = os.listdir(ruta_entrada)
    
    print("Iniciando el procesamiento por lotes...")
    
    for archivo in archivos:
        if archivo.lower().endswith(formatos_soportados):
            ruta_img_original = os.path.join(ruta_entrada, archivo)
            try:
                with Image.open(ruta_img_original) as img:
                    ancho_orig, alto_orig = img.size
                    formato_orig = img.format
                    
                    # Redimensionar (Máx 800x800)
                    img.thumbnail((800, 800))
                    
                    # Convertir a escala de grises y luego a RGB para la marca
                    img_bw = img.convert("L")
                    img_final = img_bw.convert("RGB")
                    
                    # Posición de la marca de agua (esquina inferior derecha)
                    pos_x = max(0, img_final.width - img_marca.width - 10)
                    pos_y = max(0, img_final.height - img_marca.height - 10)
                    
                    if img_marca.mode == 'RGBA':
                        img_final.paste(img_marca, (pos_x, pos_y), mask=img_marca)
                    else:
                        img_final.paste(img_marca, (pos_x, pos_y))
                    
                    ruta_guardado = os.path.join(ruta_salida, archivo)
                    img_final.save(ruta_guardado)
                    
                    worksheet.write(fila_excel, 0, archivo, formato_celda)
                    worksheet.write(fila_excel, 1, formato_orig, formato_celda)
                    worksheet.write(fila_excel, 2, ancho_orig, formato_celda)
                    worksheet.write(fila_excel, 3, alto_orig, formato_celda)
                    worksheet.write(fila_excel, 4, "Procesada", formato_celda)
                    
                    print(f"✔ {archivo} procesada con éxito.")
                    fila_excel += 1
            except Exception as e:
                print(f"❌ Error al procesar {archivo}: {e}")
                
    worksheet.set_column(0, 0, 30)
    worksheet.set_column(1, 4, 15)
    workbook.close()
    print(f"\n¡Proceso completado! Reporte generado como: '{reporte_excel}'")

if __name__ == "__main__":
    procesar_imagenes()
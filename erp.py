#%%writefile erp_streamlit.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from fpdf import FPDF

logo_path = "data:image/png;base64,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"
# Configuración inicial
st.set_page_config(page_title="Módulos del ERP", layout="wide",page_icon=logo_path)
# Ruta del archivo de imagen (logo)

# Mostrar el logo en la parte superior de la aplicación
st.image(logo_path, width=200)  # Puedes ajustar el tamaño cambiando el valor de 'width'

# Agregar un título o contenido a la aplicación
st.title("Sistema ERP")
st.write("Bienvenido al sistema ERP para la gestión de clientes, inventarios, facturación, reportes y análisis de ventas.")

st.sidebar.title("ERP_ITM")

# Variables de autenticación
USER = "Lira"
PASSWORD = "Lir@1120"

# Inicialización de variables globales
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "modulo_seleccionado" not in st.session_state:
    st.session_state["modulo_seleccionado"] = None

# Parámetros de ID
if "id_cliente" not in st.session_state:
    st.session_state["id_cliente"] = 1  # El primer ID de cliente

if "id_producto" not in st.session_state:
    st.session_state["id_producto"] = 1  # El primer ID de producto

if "id_factura" not in st.session_state:
    st.session_state["id_factura"] = 1  # El primer ID de factura

# Inicialización de DataFrames
if "clientes" not in st.session_state:
    st.session_state["clientes"] = pd.DataFrame(columns=["ID", "Nombre", "Correo", "Teléfono"])

if "productos" not in st.session_state:
    st.session_state["productos"] = pd.DataFrame(columns=["ID", "Producto", "Cantidad", "Precio Unitario"])

if "facturas" not in st.session_state:
    st.session_state["facturas"] = pd.DataFrame(columns=["Factura ID", "Cliente ID", "Cliente Nombre", "Productos", "Total", "IVA", "Fecha"])
    
# Función de autenticación
with st.sidebar:
    st.title("Módulos ERP")
if not st.session_state["auth"]:
    st.sidebar.subheader("Iniciar Sesión")
    usuario = st.sidebar.text_input("Usuario")
    contraseña = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Ingresar"):
        if usuario == USER and contraseña == PASSWORD:
            st.session_state["auth"] = True
            st.sidebar.success("Inicio de sesión exitoso.")
        else:
            st.sidebar.error("Usuario o contraseña incorrectos.")
else:
    st.sidebar.subheader(f"Bienvenido, {USER}")
    st.session_state["modulo_seleccionado"] = st.sidebar.radio(
        "Selecciona un módulo:",
        ["Gestión de Clientes", "Gestión de Inventario", "Generar Factura", "Generar Reportes", "Análisis de Ventas"],
    )
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["auth"] = False
        st.session_state["modulo_seleccionado"] = None
        st.sidebar.success("Sesión cerrada correctamente.")


# Funciones auxiliares
def exportar_csv(df, nombre_archivo):
    """Permite exportar un DataFrame como archivo CSV."""
    st.download_button(
        label="Exportar Datos",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=nombre_archivo,
        mime="text/csv",
    )

# Funciones de los módulos
def gestion_clientes():
    st.header("Gestión de Clientes")
    
    # Registro de nuevo cliente
    with st.form("Registro de Cliente"):
        nombre = st.text_input("Nombre")
        correo = st.text_input("Correo Electrónico")
        telefono = st.text_input("Teléfono")
        submitted = st.form_submit_button("Registrar Cliente")
        
        if submitted:
            # Generación de ID para el nuevo cliente
            cliente_id = st.session_state["id_cliente"]
            nuevo_cliente = pd.DataFrame([{
                "ID": cliente_id, "Nombre": nombre, "Correo": correo, "Teléfono": telefono
            }])
            st.session_state["clientes"] = pd.concat([st.session_state["clientes"], nuevo_cliente], ignore_index=True)
            st.session_state["id_cliente"] += 1  # Incrementar el ID para el siguiente cliente
            st.success(f"Cliente {nombre} registrado correctamente con ID: {cliente_id}.")
    
    # Búsqueda de clientes
    st.subheader("Buscar Cliente")
    search_term = st.text_input("Buscar por nombre o ID")
    if search_term:
        clientes_filtrados = st.session_state["clientes"][st.session_state["clientes"]["Nombre"].str.contains(search_term, case=False)]
        st.dataframe(clientes_filtrados)
    else:
        st.dataframe(st.session_state["clientes"])

    # Edición de cliente
    cliente_a_editar = st.selectbox("Seleccionar cliente para editar", st.session_state["clientes"]["ID"])
    cliente_data = st.session_state["clientes"][st.session_state["clientes"]["ID"] == cliente_a_editar]
    if cliente_data.empty:
        st.warning("Cliente no encontrado.")
    else:
        with st.form("Editar Cliente"):
            nombre_edit = st.text_input("Nuevo Nombre", cliente_data["Nombre"].values[0])
            correo_edit = st.text_input("Nuevo Correo", cliente_data["Correo"].values[0])
            telefono_edit = st.text_input("Nuevo Teléfono", cliente_data["Teléfono"].values[0])
            submitted_edit = st.form_submit_button("Actualizar Cliente")
            
            if submitted_edit:
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Nombre"] = nombre_edit
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Correo"] = correo_edit
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Teléfono"] = telefono_edit
                st.success(f"Cliente con ID {cliente_a_editar} actualizado.")

    # Eliminación de cliente
    cliente_a_eliminar = st.selectbox("Seleccionar cliente para eliminar", st.session_state["clientes"]["ID"])
    if st.button("Eliminar Cliente"):
        st.session_state["clientes"] = st.session_state["clientes"][st.session_state["clientes"]["ID"] != cliente_a_eliminar]
        st.success("Cliente eliminado correctamente.")

def gestion_inventario():

    st.header("Gestión de Inventario")
    
    # Registro de producto
    with st.form("Registro de Producto"):
        producto = st.text_input("Producto")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        precio_unitario = st.number_input("Precio Unitario", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Registrar Producto")
        
        if submitted:
            # Generación de ID para el nuevo producto
            producto_id = st.session_state["id_producto"]
            nuevo_producto = pd.DataFrame([{
                "ID": producto_id, "Producto": producto, "Cantidad": cantidad, "Precio Unitario": precio_unitario
            }])
            st.session_state["productos"] = pd.concat([st.session_state["productos"], nuevo_producto], ignore_index=True)
            st.session_state["id_producto"] += 1  # Incrementar el ID para el siguiente producto
            st.success(f"Producto {producto} registrado correctamente con ID: {producto_id}.")
    
    # Búsqueda de productos
    st.subheader("Buscar Producto")
    search_term = st.text_input("Buscar producto por nombre")
    if search_term:
        inventario_filtrado = st.session_state["productos"][st.session_state["productos"]["Producto"].str.contains(search_term, case=False)]
        st.dataframe(inventario_filtrado)
    else:
        st.dataframe(st.session_state["productos"])

    # Eliminación de producto
    producto_a_eliminar = st.selectbox("Seleccionar producto para eliminar", st.session_state["productos"]["Producto"])
    if st.button("Eliminar Producto"):
        st.session_state["productos"] = st.session_state["productos"][st.session_state["productos"]["Producto"] != producto_a_eliminar]
        st.success("Producto eliminado correctamente.")

def gestion_facturas():
    st.header("Generar Factura")
    st.write("Selecciona un cliente y productos para crear una factura.")
    
    if st.session_state["clientes"].empty:
        st.warning("No hay clientes registrados. Por favor, registra clientes antes de crear una factura.")
        return
    
    if st.session_state["productos"].empty:
        st.warning("No hay productos en el inventario. Por favor, registra productos antes de crear una factura.")
        return
    
    cliente_id = st.selectbox("Seleccionar Cliente", st.session_state["clientes"]["ID"])
    cliente_nombre = st.session_state["clientes"].loc[
        st.session_state["clientes"]["ID"] == cliente_id, "Nombre"
    ].values[0]
    
    # Selección de productos
    productos_seleccionados = st.multiselect(
        "Selecciona productos", 
        st.session_state["productos"]["Producto"].values
    )
    
    if not productos_seleccionados:
        st.info("Selecciona al menos un producto para generar una factura.")
        return
    
    productos_detalle = []
    total = 0
    
    for producto in productos_seleccionados:
        producto_info = st.session_state["productos"].loc[
            st.session_state["productos"]["Producto"] == producto
        ]
        precio_unitario = producto_info["Precio Unitario"].values[0]
        stock_disponible = producto_info["Cantidad"].values[0]
        
        # Selección de cantidad
        cantidad = st.number_input(
            f"Cantidad de {producto} (Disponible: {stock_disponible})", 
            min_value=1, 
            max_value=stock_disponible, 
            step=1
        )
        
        subtotal = precio_unitario * cantidad
        total += subtotal
        productos_detalle.append({
            "Producto": producto,
            "Cantidad": cantidad,
            "Precio Unitario": precio_unitario,
            "Subtotal": subtotal
        })
    
    # Calcular IVA y total final
    iva = total * 0.16
    total_con_iva = total + iva
    
    # Mostrar resumen
    st.subheader("Resumen de Factura")
    st.table(pd.DataFrame(productos_detalle))
    st.write(f"Subtotal: ${total:,.2f}")
    st.write(f"IVA (16%): ${iva:,.2f}")
    st.write(f"Total: ${total_con_iva:,.2f}")
    
    # Confirmación y registro de factura
    if st.button("Confirmar y Generar Factura"):
        factura_id = st.session_state["id_factura"]
        fecha = pd.to_datetime("today").strftime("%Y-%m-%d")
        
        # Registrar factura
        factura = pd.DataFrame([{
            "Factura ID": factura_id, 
            "Cliente ID": cliente_id, 
            "Cliente Nombre": cliente_nombre,
            "Productos": productos_detalle, 
            "Total": total, 
            "IVA": iva, 
            "Fecha": fecha
        }])
        st.session_state["facturas"] = pd.concat([st.session_state["facturas"], factura], ignore_index=True)
        st.session_state["id_factura"] += 1  # Incrementar el ID para la siguiente factura
        
        # Reducir inventario
        for detalle in productos_detalle:
            producto = detalle["Producto"]
            cantidad = detalle["Cantidad"]
            st.session_state["productos"].loc[
                st.session_state["productos"]["Producto"] == producto, "Cantidad"
            ] -= cantidad
        
        st.success(f"Factura {factura_id} generada correctamente.")
        st.write(f"Total con IVA: ${total_con_iva:,.2f}")
        
        # Exportar factura
        exportar_csv(st.session_state["facturas"], f"factura_{factura_id}.csv")

def gestion_reportes():
 

    st.header("Generar Reportes")

    # Generación de reportes contables
    st.write("Aquí pueden ir los reportes contables.")
    st.write("Funciones específicas para reportes como ingresos, gastos y balances se agregarán aquí.")
    
    # Simulando el reporte básico
    st.text_area("Resumen", "Reporte generado: ingresos, gastos, balance general, etc.")
    
    # Exportar el reporte a CSV
    exportar_csv(st.session_state["facturas"], "reportes_contables.csv")

import plotly.express as px

def analisis_ventas():
    st.header("Análisis de Ventas")
    
    # Verificar si hay datos en las facturas
    if st.session_state["facturas"].empty:
        st.warning("No hay datos de facturas para analizar.")
        return

    # Crear una lista para desglosar productos en facturas
    productos_desglosados = []
    for _, fila in st.session_state["facturas"].iterrows():
        for producto in fila["Productos"]:
            productos_desglosados.append({
                "Producto": producto["Producto"],
                "Cantidad": producto["Cantidad"],
                "Subtotal": producto["Subtotal"],
                "Fecha": fila["Fecha"]
            })

    # Crear un DataFrame con los datos desglosados
    df_productos = pd.DataFrame(productos_desglosados)

    # Verificar si hay datos en el DataFrame desglosado
    if df_productos.empty:
        st.warning("No hay datos suficientes para generar análisis.")
        return

    # Análisis de ventas por producto
    st.subheader("Ventas por Producto")
    ventas_por_producto = df_productos.groupby("Producto").sum().reset_index()
    fig1 = px.bar(
        ventas_por_producto, 
        x="Producto", 
        y="Subtotal", 
        title="Ingresos por Producto", 
        labels={"Subtotal": "Ingresos ($)"},
        text="Subtotal"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Análisis de cantidades vendidas por producto
    st.subheader("Cantidad Vendida por Producto")
    fig2 = px.pie(
        ventas_por_producto, 
        names="Producto", 
        values="Cantidad", 
        title="Distribución de Cantidades Vendidas"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Análisis temporal de ventas
    st.subheader("Ingresos Totales por Fecha")
    df_productos["Fecha"] = pd.to_datetime(df_productos["Fecha"])
    ingresos_por_fecha = df_productos.groupby("Fecha").sum().reset_index()
    fig3 = px.line(
        ingresos_por_fecha, 
        x="Fecha", 
        y="Subtotal", 
        title="Evolución de Ingresos en el Tiempo",
        labels={"Subtotal": "Ingresos ($)", "Fecha": "Fecha"}
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.success("Gráficos interactivos generados correctamente.")

# Navegación entre módulos
if st.session_state["auth"]:
    if st.session_state["modulo_seleccionado"] == "Gestión de Clientes":
        gestion_clientes()
    elif st.session_state["modulo_seleccionado"] == "Gestión de Inventario":
        gestion_inventario()
    elif st.session_state["modulo_seleccionado"] == "Generar Factura":
        gestion_facturas()
    elif st.session_state["modulo_seleccionado"] == "Generar Reportes":
        gestion_reportes()
    elif st.session_state["modulo_seleccionado"] == "Análisis de Ventas":
        analisis_ventas()
else:
    st.warning("Por favor, inicia sesión para continuar.")

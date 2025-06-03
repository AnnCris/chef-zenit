from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from app.models.receta import Receta
from app.services.recomendacion import SistemaRecomendacion
import io
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFGenerator:
    """
    Generador de PDFs para recetas y recomendaciones nutricionales
    """
    
    def __init__(self):
        self.sistema_recomendacion = SistemaRecomendacion()
        self.styles = getSampleStyleSheet()
        
        # Definir estilos personalizados
        self.title_style = ParagraphStyle(
            name='TitleStyle',
            parent=self.styles['Title'],
            alignment=TA_CENTER,
            fontSize=20,
            spaceAfter=12
        )
        
        self.subtitle_style = ParagraphStyle(
            name='SubtitleStyle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=8,
            spaceBefore=16
        )
        
        self.section_style = ParagraphStyle(
            name='SectionStyle',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceBefore=12,
            spaceAfter=6
        )
        
        self.normal_style = ParagraphStyle(
            name='NormalStyle',
            parent=self.styles['Normal'],
            fontSize=11
        )
        
        self.list_item_style = ParagraphStyle(
            name='ListItemStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            leftIndent=20
        )
    
    def generar_pdf_receta(self, receta_id, include_nutrition=True, include_substitutes=True):
        """
        Genera un PDF con la información de una receta
        
        Args:
            receta_id: ID de la receta
            include_nutrition: Incluir información nutricional
            include_substitutes: Incluir sustitutos para ingredientes
            
        Returns:
            Bytes del PDF generado
        """
        # Obtener la receta
        receta = Receta.query.get(receta_id)
        
        if not receta:
            logger.error(f"No se encontró la receta con ID {receta_id}")
            return None
            
        # Crear un buffer para el PDF
        buffer = io.BytesIO()
        
        # Configurar el documento
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Lista para almacenar los elementos del PDF
        elements = []
        
        # Título
        elements.append(Paragraph(receta.nombre, self.title_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Imagen (si existe)
        if receta.imagen_url:
            img_path = os.path.join('app', receta.imagen_url)
            if os.path.exists(img_path):
                try:
                    img = Image(img_path, width=4*inch, height=3*inch)
                    elements.append(img)
                    elements.append(Spacer(1, 0.25*inch))
                except Exception as e:
                    logger.error(f"Error al incluir imagen: {str(e)}")
        
        # Descripción
        if receta.descripcion:
            elements.append(Paragraph("Descripción:", self.section_style))
            elements.append(Paragraph(receta.descripcion, self.normal_style))
            elements.append(Spacer(1, 0.25*inch))
        
        # Información general
        info_data = [
            ["Tiempo de preparación:", f"{receta.tiempo_preparacion} minutos"],
            ["Porciones:", f"{receta.porciones}"],
            ["Dificultad:", receta.dificultad or "Media"],
            ["Categoría:", receta.categoria or "General"]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.25*inch))
        
        # Ingredientes
        elements.append(Paragraph("Ingredientes:", self.section_style))
        
        ingredientes_data = []
        # Encabezados
        ingredientes_data.append(["Ingrediente", "Cantidad", "Unidad"])
        
        # Filas de ingredientes
        for ri in receta.ingredientes:
            nombre = ri.ingrediente.nombre
            if ri.es_opcional:
                nombre += " (opcional)"
            
            ingredientes_data.append([
                nombre,
                str(ri.cantidad) if ri.cantidad else "",
                ri.unidad or ""
            ])
        
        # Crear tabla de ingredientes
        ingredientes_table = Table(ingredientes_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        ingredientes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        
        elements.append(ingredientes_table)
        elements.append(Spacer(1, 0.25*inch))
        
        # Pasos de preparación
        elements.append(Paragraph("Preparación:", self.section_style))
        
        for paso in receta.pasos:
            texto_paso = f"{paso.numero_paso}. {paso.descripcion}"
            elements.append(Paragraph(texto_paso, self.list_item_style))
            elements.append(Spacer(1, 0.1*inch))
        
        # Información nutricional
        if include_nutrition:
            elements.append(Spacer(1, 0.25*inch))
            elements.append(Paragraph("Información Nutricional:", self.section_style))
            
            # Información básica
            info_nutri_data = [
                ["Calorías:", f"{receta.calorias or 0} kcal"],
                ["Proteínas:", f"{receta.proteinas or 0} g"],
                ["Carbohidratos:", f"{receta.carbohidratos or 0} g"],
                ["Grasas:", f"{receta.grasas or 0} g"]
            ]
            
            # Obtener información nutricional detallada
            nutri_info = self.sistema_recomendacion.obtener_informacion_nutricional(receta_id)
            
            if nutri_info and 'vitaminas' in nutri_info:
                # Agregar información de vitaminas
                for vit, valor in nutri_info['vitaminas'].items():
                    if valor:
                        info_nutri_data.append([f"Vitamina {vit}:", f"{valor} μg"])
            
            if nutri_info and 'minerales' in nutri_info:
                # Agregar información de minerales
                for mineral, valor in nutri_info['minerales'].items():
                    if valor:
                        info_nutri_data.append([f"{mineral.capitalize()}:", f"{valor} mg"])
            
            # Crear tabla nutricional
            nutri_table = Table(info_nutri_data, colWidths=[2*inch, 3*inch])
            nutri_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]))
            
            elements.append(nutri_table)
        
        # Sustitutos para ingredientes
        if include_substitutes:
            has_substitutes = False
            substitutes_data = []
            
            # Encabezados
            substitutes_data.append(["Ingrediente original", "Sustituto", "Tipo", "Notas"])
            
            # Obtener sustitutos para cada ingrediente
            for ri in receta.ingredientes:
                sustitutos = self.sistema_recomendacion.obtener_sustitutos(ri.ingrediente.id)
                
                if sustitutos:
                    has_substitutes = True
                    
                    for sustituto in sustitutos:
                        sustitucion = sustituto.get('sustitucion', {})
                        substitutes_data.append([
                            ri.ingrediente.nombre,
                            sustituto.get('nombre', ''),
                            sustitucion.get('tipo_sustitucion', ''),
                            sustitucion.get('notas', '')
                        ])
            
            if has_substitutes:
                elements.append(Spacer(1, 0.25*inch))
                elements.append(Paragraph("Sustitutos de Ingredientes:", self.section_style))
                
                # Crear tabla de sustitutos
                substitutes_table = Table(substitutes_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 2.5*inch])
                substitutes_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                    ('TOPPADDING', (0, 1), (-1, -1), 6),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                
                elements.append(substitutes_table)
        
        # Construir el PDF
        doc.build(elements)
        
        # Obtener el contenido del buffer
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
    
    def generar_pdf_recomendaciones(self, recetas_ids, titulo="Recetas Recomendadas"):
        """
        Genera un PDF con múltiples recetas recomendadas
        
        Args:
            recetas_ids: Lista de IDs de recetas
            titulo: Título del PDF
            
        Returns:
            Bytes del PDF generado
        """
        # Verificar que haya recetas
        if not recetas_ids:
            logger.error("No se proporcionaron IDs de recetas")
            return None
            
        # Crear un buffer para el PDF
        buffer = io.BytesIO()
        
        # Configurar el documento
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Lista para almacenar los elementos del PDF
        elements = []
        
        # Título principal
        elements.append(Paragraph(titulo, self.title_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # Procesar cada receta
        for i, receta_id in enumerate(recetas_ids):
            receta = Receta.query.get(receta_id)
            
            if not receta:
                continue
                
            # Si no es la primera receta, agregar un salto de página
            if i > 0:
                elements.append(Spacer(1, 0.5*inch))
                elements.append(Paragraph("", self.normal_style))
                elements.append(Spacer(1, 0.5*inch))
            
            # Título de la receta
            elements.append(Paragraph(receta.nombre, self.subtitle_style))
            elements.append(Spacer(1, 0.25*inch))
            
            # Imagen (si existe)
            if receta.imagen_url:
                img_path = os.path.join('app', receta.imagen_url)
                if os.path.exists(img_path):
                    try:
                        img = Image(img_path, width=4*inch, height=3*inch)
                        elements.append(img)
                        elements.append(Spacer(1, 0.25*inch))
                    except Exception as e:
                        logger.error(f"Error al incluir imagen: {str(e)}")
            
            # Descripción
            if receta.descripcion:
                elements.append(Paragraph("Descripción:", self.section_style))
                elements.append(Paragraph(receta.descripcion, self.normal_style))
                elements.append(Spacer(1, 0.25*inch))
            
            # Información general
            info_data = [
                ["Tiempo:", f"{receta.tiempo_preparacion} min"],
                ["Porciones:", f"{receta.porciones}"],
                ["Dificultad:", receta.dificultad or "Media"],
            ]
            
            info_table = Table(info_data, colWidths=[1.5*inch, 2*inch])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]))
            
            elements.append(info_table)
            elements.append(Spacer(1, 0.25*inch))
            
            # Ingredientes (versión resumida)
            elements.append(Paragraph("Ingredientes:", self.section_style))
            
            for ri in receta.ingredientes:
                nombre = ri.ingrediente.nombre
                cantidad = f"{ri.cantidad} {ri.unidad}" if ri.cantidad and ri.unidad else ""
                
                if ri.es_opcional:
                    nombre += " (opcional)"
                
                texto_ingrediente = f"• {nombre}"
                if cantidad:
                    texto_ingrediente += f": {cantidad}"
                    
                elements.append(Paragraph(texto_ingrediente, self.list_item_style))
            
            elements.append(Spacer(1, 0.25*inch))
            
            # Información nutricional básica
            elements.append(Paragraph("Nutrición:", self.section_style))
            
            nutri_data = [
                ["Calorías:", f"{receta.calorias or 0} kcal"],
                ["Proteínas:", f"{receta.proteinas or 0} g"],
                ["Carbohidratos:", f"{receta.carbohidratos or 0} g"],
                ["Grasas:", f"{receta.grasas or 0} g"]
            ]
            
            nutri_table = Table(nutri_data, colWidths=[1.5*inch, 2*inch])
            nutri_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]))
            
            elements.append(nutri_table)
        
        # Construir el PDF
        doc.build(elements)
        
        # Obtener el contenido del buffer
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
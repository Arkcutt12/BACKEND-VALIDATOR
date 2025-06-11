# 📋 Catálogo de Errores DXF Analyzer

## 🔴 Errores Críticos

### 1. Vectores Abiertos
**Descripción:** Polilíneas sin cerrar en capas de corte o grabado.
**Causa:** Mal uso de 'Join'/'Cerrar ruta' en el software de diseño.
**Solución:** Cerrar todas las polilíneas en capas de corte.
**Severidad:** 10/10

### 2. Vectores Sin Capa
**Descripción:** Elementos sin asignación clara de capa.
**Causa:** Olvido al diseñar o elementos en capa por defecto.
**Solución:** Asignar todos los elementos a capas específicas.
**Severidad:** 9/10

### 3. Texto Editable
**Descripción:** Texto encontrado sin convertir a curvas.
**Causa:** No se han convertido las fuentes a contornos vectoriales.
**Solución:** Convertir todos los textos a curvas/contornos.
**Severidad:** 8/10

### 4. Capas Incorrectas
**Descripción:** Nombres de capas no reconocidos.
**Causa:** Uso de nombres de capas personalizados.
**Solución:** Usar nombres estándar: CUT, ENGRAVE, MARK, etc.
**Severidad:** 7/10

### 5. Objetos Fuera de Área
**Descripción:** Geometrías alejadas del origen o fuera del área de trabajo.
**Causa:** Pegado de objetos externos o errores de escala.
**Solución:** Mover todos los objetos cerca del origen (0,0).
**Severidad:** 8/10

### 6. Capas Invisibles
**Descripción:** Objetos en capas ocultas o bloqueadas.
**Causa:** Capa oculta accidentalmente.
**Solución:** Activar visibilidad de todas las capas necesarias.
**Severidad:** 8/10

### 7. Vectores Duplicados
**Descripción:** Dos o más vectores idénticos superpuestos.
**Causa:** Copiado sin borrar el original.
**Solución:** Eliminar vectores duplicados.
**Severidad:** 7/10

### 8. Capas Mezcladas
**Descripción:** Elementos de grabado y corte en misma capa.
**Causa:** Mezcla accidental de procesos.
**Solución:** Separar elementos por proceso en capas distintas.
**Severidad:** 9/10

### 9. Grosor de Línea
**Descripción:** Vectores con linewidth definido.
**Causa:** Exportación incorrecta con grosor de línea.
**Solución:** Exportar con grosor de línea 0 o 'ByLayer'.
**Severidad:** 6/10

### 10. Unidades Incorrectas
**Descripción:** Archivo en pulgadas en vez de milímetros.
**Causa:** Configuración incorrecta de unidades.
**Solución:** Exportar en milímetros (mm).
**Severidad:** 9/10

## ⚠️ Advertencias

### 11. Escala Incorrecta
**Descripción:** Elementos <5mm o >3000mm.
**Causa:** Escala incorrecta o unidades mal configuradas.
**Solución:** Verificar dimensiones y escala.
**Severidad:** 4/10

### 12. Corte Interno Desalineado
**Descripción:** Elementos internos fuera del objeto.
**Causa:** Desalineación en el diseño.
**Solución:** Alinear elementos internos correctamente.
**Severidad:** 5/10

### 13. Textos Muy Pequeños
**Descripción:** Letras ilegibles al grabar.
**Causa:** Tamaño de texto insuficiente.
**Solución:** Aumentar tamaño mínimo a 2mm.
**Severidad:** 3/10

### 14. Curvas Excesivas
**Descripción:** Grabado muy lento o impreciso.
**Causa:** Demasiadas subdivisiones en curvas.
**Solución:** Simplificar curvas complejas.
**Severidad:** 4/10

### 15. Capas de Referencia
**Descripción:** Elementos en capas guía.
**Causa:** Elementos en capas que no deberían exportarse.
**Solución:** Eliminar elementos de capas de referencia.
**Severidad:** 3/10

### 16. Objetos en Bloques
**Descripción:** Entidades ocultas en blocks.
**Causa:** Uso de bloques sin explotar.
**Solución:** Explotar todos los bloques.
**Severidad:** 5/10

### 17. Colores vs Capas
**Descripción:** Uso de colores para definir procesos.
**Causa:** Confusión entre colores y capas.
**Solución:** Usar capas para definir procesos.
**Severidad:** 4/10

### 18. Puntos Redundantes
**Descripción:** Polilíneas con muchos nodos.
**Causa:** Muchas subdivisiones generan ruido.
**Solución:** Simplificar curva para reducir puntos.
**Severidad:** 4/10

### 19. Vectores de Imágenes
**Descripción:** Trazados mal vectorizados.
**Causa:** Vectorización automática de baja calidad.
**Solución:** Mejorar vectorización o redibujar.
**Severidad:** 5/10

## 📤 Errores de Exportación

### 20. Versión DXF
**Descripción:** Formato muy nuevo o no compatible.
**Causa:** Versión muy nueva del formato DXF.
**Solución:** Exportar como DXF R2010 o R2013.
**Severidad:** 6/10

### 21. Formato No Vectorial
**Descripción:** Imagen embebida en lugar de vectores.
**Causa:** Exportación incorrecta o archivo mixto.
**Solución:** Convertir todo a vectores antes de exportar.
**Severidad:** 7/10

### 22. Coordenadas Z
**Descripción:** Entidades con valores Z ≠ 0.
**Causa:** Diseño en 3D o exportación incorrecta.
**Solución:** Aplanar todas las entidades al plano Z=0.
**Severidad:** 5/10

### 23. Objetos Agrupados
**Descripción:** Groups o blocks anidados.
**Causa:** Estructura compleja del archivo.
**Solución:** Explotar todos los grupos y bloques.
**Severidad:** 6/10

### 24. Archivo Pesado
**Descripción:** Demasiados nodos innecesarios.
**Causa:** Mala vectorización o elementos complejos.
**Solución:** Simplificar curvas y reducir nodos.
**Severidad:** 6/10

## 🎯 Mejores Prácticas

### Preparación de Archivos
1. Exportar como DXF R2010 o R2013
2. Usar nombres de capas estándar
3. Convertir textos a curvas
4. Cerrar todas las polilíneas
5. Explotar bloques y grupos
6. Aplanar al plano Z=0
7. Usar unidades en milímetros
8. Limpiar elementos innecesarios

### Optimización
1. Simplificar curvas complejas
2. Eliminar nodos redundantes
3. Unir elementos superpuestos
4. Limpiar capas no utilizadas
5. Verificar dimensiones
6. Revisar alineaciones
7. Optimizar para corte láser

### Exportación
1. Verificar versión DXF
2. Comprobar unidades
3. Revisar capas
4. Validar geometrías
5. Limpiar archivo
6. Probar en software de corte
7. Documentar cambios 
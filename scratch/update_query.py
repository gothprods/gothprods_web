import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Buscamos interactions_query y le inyectamos los filtros
original_query = """    interactions_query = '''
    SELECT id, section, title, COALESCE(views, 0) as views, COALESCE(likes, 0) as likes, 
           created_at, 'content' as item_type
    FROM content_items 
    WHERE section IN ('El Noticiero Nocturno', 'Reseñas de Conciertos')
    
    UNION ALL
    
    SELECT id, 'Banda de la Semana' as section, nombre as title, COALESCE(views, 0) as views, COALESCE(likes, 0) as likes,
           created_at, 'banda' as item_type
    FROM banda_semana
    
    UNION ALL
    
    SELECT id, 'Agenda Metalera' as section, titulo_articulo as title, COALESCE(views, 0) as views, COALESCE(likes, 0) as likes,
           created_at, 'evento' as item_type
    FROM eventos_semana
    
    ORDER BY id DESC, created_at DESC
    '''
    interactions_rows = conn.execute(interactions_query).fetchall()"""

new_query = """    date_filter = ""
    date_params = []
    
    if perf_range == '7':
        date_filter = " AND created_at >= datetime('now', '-7 days')"
    elif perf_range == '30':
        date_filter = " AND created_at >= datetime('now', '-30 days')"
    elif perf_range == '90':
        date_filter = " AND created_at >= datetime('now', '-90 days')"
    elif perf_range == 'custom' and perf_start and perf_end:
        date_filter = " AND created_at >= ? AND created_at <= ?"
        date_params = [perf_start + ' 00:00:00', perf_end + ' 23:59:59']
        
    interactions_query = f'''
    SELECT id, section, title, COALESCE(views, 0) as views, COALESCE(likes, 0) as likes, 
           created_at, 'content' as item_type
    FROM content_items 
    WHERE section IN ('El Noticiero Nocturno', 'Reseñas de Conciertos'){date_filter}
    
    UNION ALL
    
    SELECT id, 'Banda de la Semana' as section, nombre as title, COALESCE(views, 0) as views, COALESCE(likes, 0) as likes,
           created_at, 'banda' as item_type
    FROM banda_semana
    WHERE 1=1{date_filter}
    
    UNION ALL
    
    SELECT id, 'Agenda Metalera' as section, titulo_articulo as title, COALESCE(views, 0) as views, COALESCE(likes, 0) as likes,
           created_at, 'evento' as item_type
    FROM eventos_semana
    WHERE 1=1{date_filter}
    
    ORDER BY created_at DESC, id DESC
    '''
    
    # We need to duplicate date_params for each UNION ALL block (3 blocks)
    full_params = date_params * 3
    interactions_rows = conn.execute(interactions_query, full_params).fetchall()"""

content = content.replace(original_query, new_query)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Query Updated.")

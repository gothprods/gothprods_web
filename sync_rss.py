import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import sqlite3
import datetime
import sys

DB_PATH = "gothprods.db"

def fetch_xml(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return response.read()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def is_link_alive(url):
    if not url: return True
    if "youtube.com" in url or "youtu.be" in url:
        check_url = "https://www.youtube.com/oembed?url=" + url
    else:
        check_url = url
        
    try:
        req = urllib.request.Request(check_url, method="HEAD", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as response:
            return response.status < 400
    except urllib.error.HTTPError as e:
        if e.code in [404, 401, 403, 400]:
            return False
        return True # Assume alive on rate limits or other errors
    except Exception:
        return True # Do not delete on random connection issues

def cleanup_dead_links(conn, sections):
    c = conn.cursor()
    placeholders = ','.join(['?']*len(sections))
    c.execute(f"SELECT id, yt_link, ap_link, title FROM content_items WHERE section IN ({placeholders})", sections)
    rows = c.fetchall()
    
    deleted_count = 0
    for row in rows:
        item_id, yt_link, ap_link, title = row
        link_to_check = yt_link if yt_link else ap_link
        if link_to_check:
            if not is_link_alive(link_to_check):
                print(f"Deleting removed item '{title}' ({link_to_check})")
                c.execute("DELETE FROM content_items WHERE id = ?", (item_id,))
                deleted_count += 1
                
    if deleted_count > 0:
        conn.commit()

def sync_youtube(target_section):
    print(f"Syncing YouTube for {target_section}...")
    url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCpFYBWWYJHgD5U0olc88s9A"
    xml_data = fetch_xml(url)
    if not xml_data: return

    root = ET.fromstring(xml_data)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    sections_synced = set()

    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        yt_link = entry.find('{http://www.w3.org/2005/Atom}link').attrib['href']
        
        media_group = entry.find('{http://search.yahoo.com/mrss/}group')
        desc = media_group.find('{http://search.yahoo.com/mrss/}description').text if media_group is not None else ""
        thumbnail = media_group.find('{http://search.yahoo.com/mrss/}thumbnail').attrib['url'] if media_group is not None else "assets/logo.png"
        
        if not desc or desc.strip() == "":
            if "live" in title.lower() or "en vivo" in title.lower():
                desc = f"Transmisión en vivo: {title}. ¡Únete al debate y análisis de la escena del metal!"
            else:
                desc = f"Disfruta de este episodio: {title}. Suscríbete y no te pierdas el mejor contenido de Goth Prods."

        section = "La Galería Nocturna"
        title_lower = title.lower()
        if "caos sonoro" in title_lower:
            section = "Caos Sonoro"
        elif "metal pulse" in title_lower:
            section = "Metal Pulse"
        elif "colaboraci" in title_lower or "collab" in title_lower:
            section = "Colaboraciones"

        if target_section == "La Galería Nocturna":
            if section not in ("La Galería Nocturna", "Caos Sonoro", "Colaboraciones"):
                continue
        else:
            if section != target_section:
                continue
                
        sections_synced.add(section)
        short_desc = (desc[:150] + "...") if len(desc) > 150 else desc

        from email.utils import parsedate_to_datetime
        published = entry.find('{http://www.w3.org/2005/Atom}published')
        if published is not None:
            pub_date = published.text.replace('T', ' ')[:19]
        else:
            pub_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        c.execute("SELECT id, image_filename, short_desc FROM content_items WHERE yt_link = ? OR title = ?", (yt_link, title))
        row = c.fetchone()
        if row:
            item_id, current_image, current_short = row
            
            # Decide whether to update short_desc
            update_desc = False
            if not current_short or current_short.strip() == "":
                update_desc = True
            elif "Transmisión en vivo" in current_short or "Disfruta de este episodio" in current_short:
                update_desc = True
                
            if not current_image or current_image == "assets/logo.png" or current_image.startswith('http'):
                if update_desc:
                    c.execute("UPDATE content_items SET title = ?, yt_link = ?, created_at = ?, image_filename = ?, section = ?, short_desc = ? WHERE id = ?", (title, yt_link, pub_date, thumbnail, section, short_desc, item_id))
                else:
                    c.execute("UPDATE content_items SET title = ?, yt_link = ?, created_at = ?, image_filename = ?, section = ? WHERE id = ?", (title, yt_link, pub_date, thumbnail, section, item_id))
            else:
                if update_desc:
                    c.execute("UPDATE content_items SET title = ?, yt_link = ?, created_at = ?, section = ?, short_desc = ? WHERE id = ?", (title, yt_link, pub_date, section, short_desc, item_id))
                else:
                    c.execute("UPDATE content_items SET title = ?, yt_link = ?, created_at = ?, section = ? WHERE id = ?", (title, yt_link, pub_date, section, item_id))
        else:
            c.execute('''INSERT INTO content_items 
                         (section, title, short_desc, image_filename, yt_link, created_at)
                         VALUES (?, ?, ?, ?, ?, ?)''', 
                      (section, title, short_desc, thumbnail, yt_link, pub_date))
    conn.commit()
    
    if target_section == "La Galería Nocturna":
        cleanup_dead_links(conn, ("La Galería Nocturna", "Caos Sonoro", "Colaboraciones"))
    else:
        cleanup_dead_links(conn, (target_section,))
        
    conn.close()

def sync_youtube_playlist(playlist_id, target_section):
    print(f"Syncing YouTube Playlist {playlist_id} for {target_section}...")
    url = f"https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}"
    xml_data = fetch_xml(url)
    if not xml_data: return

    root = ET.fromstring(xml_data)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        yt_link = entry.find('{http://www.w3.org/2005/Atom}link').attrib['href']
        
        media_group = entry.find('{http://search.yahoo.com/mrss/}group')
        desc = media_group.find('{http://search.yahoo.com/mrss/}description').text if media_group is not None else ""
        thumbnail = media_group.find('{http://search.yahoo.com/mrss/}thumbnail').attrib['url'] if media_group is not None else "assets/logo.png"
        
        if not desc or desc.strip() == "":
            desc = f"Disfruta de este episodio: {title}. Suscríbete y no te pierdas el mejor contenido de Goth Prods."

        short_desc = (desc[:150] + "...") if len(desc) > 150 else desc

        published = entry.find('{http://www.w3.org/2005/Atom}published')
        if published is not None:
            pub_date = published.text.replace('T', ' ')[:19]
        else:
            pub_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        c.execute("SELECT id, image_filename FROM content_items WHERE yt_link = ? OR title = ?", (yt_link, title))
        row = c.fetchone()
        if row:
            current_image = row[1]
            if not current_image or current_image == "assets/logo.png" or current_image.startswith('http'):
                c.execute("UPDATE content_items SET title = ?, yt_link = ?, created_at = ?, image_filename = ?, section = ? WHERE id = ?", (title, yt_link, pub_date, thumbnail, target_section, row[0]))
            else:
                c.execute("UPDATE content_items SET title = ?, yt_link = ?, created_at = ?, section = ? WHERE id = ?", (title, yt_link, pub_date, target_section, row[0]))
        else:
            c.execute('''INSERT INTO content_items 
                         (section, title, short_desc, image_filename, yt_link, created_at)
                         VALUES (?, ?, ?, ?, ?, ?)''', 
                      (target_section, title, short_desc, thumbnail, yt_link, pub_date))
    
    conn.commit()
    cleanup_dead_links(conn, (target_section,))
    conn.close()

def sync_ivoox(url, section):
    print(f"Syncing Ivoox for {section}...")
    xml_data = fetch_xml(url)
    if not xml_data: return

    root = ET.fromstring(xml_data)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for item in root.findall('.//item'):
        title = item.find('title').text
        link = item.find('link').text
        
        itunes_image = item.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}image')
        thumbnail = itunes_image.get('href') if itunes_image is not None else "assets/logo.png"
        
        desc = item.find('description').text or ""
        desc = desc.replace("<p>", "").replace("</p>", "").replace("<br/>", "")
        
        if not desc or desc.strip() == "":
            desc = f"Escucha este episodio de podcast: {title}. ¡No te lo pierdas!"
            
        short_desc = (desc[:150] + "...") if len(desc) > 150 else desc

        from email.utils import parsedate_to_datetime
        pubDate = item.find('pubDate')
        if pubDate is not None:
            try:
                dt = parsedate_to_datetime(pubDate.text)
                pub_date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                pub_date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            pub_date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        c.execute("SELECT id, image_filename FROM content_items WHERE ap_link = ? OR title = ?", (link, title))
        row = c.fetchone()
        if row:
            current_image = row[1]
            if not current_image or current_image == "assets/logo.png" or current_image.startswith('http'):
                c.execute("UPDATE content_items SET title = ?, ap_link = ?, created_at = ?, image_filename = ?, section = ? WHERE id = ?", (title, link, pub_date_str, thumbnail, section, row[0]))
            else:
                c.execute("UPDATE content_items SET title = ?, ap_link = ?, created_at = ?, section = ? WHERE id = ?", (title, link, pub_date_str, section, row[0]))
        else:
            c.execute('''INSERT INTO content_items 
                         (section, title, short_desc, image_filename, ap_link, created_at)
                         VALUES (?, ?, ?, ?, ?, ?)''', 
                      (section, title, short_desc, thumbnail, link, pub_date_str))

    conn.commit()
    cleanup_dead_links(conn, (section,))
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if target == "galeria":
            sync_youtube("La Galería Nocturna")
        elif target == "metal_pulse":
            sync_ivoox("https://feeds.ivoox.com/feed_fg_f12064367_filtro_1.xml", "Metal Pulse")
        elif target == "entrevistas":
            sync_youtube_playlist("PLvx0zBV_ivqAdRE2WhzwUscz1RfR4W9US", "Entrevistas Under")
    else:
        sync_youtube("La Galería Nocturna")
        sync_ivoox("https://feeds.ivoox.com/feed_fg_f12064367_filtro_1.xml", "Metal Pulse")
        sync_youtube_playlist("PLvx0zBV_ivqAdRE2WhzwUscz1RfR4W9US", "Entrevistas Under")
    print("Sync complete!")

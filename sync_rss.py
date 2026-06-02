import urllib.request
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

def sync_youtube(target_section):
    print(f"Syncing YouTube for {target_section}...")
    url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCpFYBWWYJHgD5U0olc88s9A"
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

        # Determine section based on title
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

        short_desc = (desc[:150] + "...") if desc and len(desc) > 150 else desc

        # Date parsing
        from email.utils import parsedate_to_datetime
        published = entry.find('{http://www.w3.org/2005/Atom}published')
        if published is not None:
            # Format: 2021-01-11T02:08:47+00:00
            pub_date = published.text.replace('T', ' ')[:19]
        else:
            pub_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Check if exists to prevent duplication
        c.execute("SELECT id, image_filename FROM content_items WHERE yt_link = ? OR title = ?", (yt_link, title))
        row = c.fetchone()
        if row:
            # Update only created_at, title, and yt_link to avoid overwriting manually uploaded custom thumbnails
            current_image = row[1]
            if current_image == "assets/logo.png" or not current_image:
                c.execute("UPDATE content_items SET title = ?, yt_link = ?, created_at = ?, image_filename = ?, section = ? WHERE id = ?", (title, yt_link, pub_date, thumbnail, section, row[0]))
            else:
                c.execute("UPDATE content_items SET title = ?, yt_link = ?, created_at = ?, section = ? WHERE id = ?", (title, yt_link, pub_date, section, row[0]))
        else:
            c.execute('''INSERT INTO content_items 
                         (section, title, short_desc, image_filename, yt_link, created_at)
                         VALUES (?, ?, ?, ?, ?, ?)''', 
                      (section, title, short_desc, thumbnail, yt_link, pub_date))
    conn.commit()
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

        short_desc = (desc[:150] + "...") if desc and len(desc) > 150 else desc

        published = entry.find('{http://www.w3.org/2005/Atom}published')
        if published is not None:
            pub_date = published.text.replace('T', ' ')[:19]
        else:
            pub_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        c.execute("SELECT id, image_filename FROM content_items WHERE yt_link = ? OR title = ?", (yt_link, title))
        row = c.fetchone()
        if row:
            current_image = row[1]
            if current_image == "assets/logo.png" or not current_image:
                c.execute("UPDATE content_items SET title = ?, yt_link = ?, created_at = ?, image_filename = ?, section = ? WHERE id = ?", (title, yt_link, pub_date, thumbnail, target_section, row[0]))
            else:
                c.execute("UPDATE content_items SET title = ?, yt_link = ?, created_at = ?, section = ? WHERE id = ?", (title, yt_link, pub_date, target_section, row[0]))
        else:
            c.execute('''INSERT INTO content_items 
                         (section, title, short_desc, image_filename, yt_link, created_at)
                         VALUES (?, ?, ?, ?, ?, ?)''', 
                      (target_section, title, short_desc, thumbnail, yt_link, pub_date))
    
    conn.commit()
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
        link = item.find('link').text # Ivoox link
        
        itunes_image = item.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}image')
        thumbnail = itunes_image.get('href') if itunes_image is not None else "assets/logo.png"
        
        desc = item.find('description').text or ""
        desc = desc.replace("<p>", "").replace("</p>", "").replace("<br/>", "")
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
            if current_image == "assets/logo.png" or not current_image:
                c.execute("UPDATE content_items SET title = ?, ap_link = ?, created_at = ?, image_filename = ?, section = ? WHERE id = ?", (title, link, pub_date_str, thumbnail, section, row[0]))
            else:
                c.execute("UPDATE content_items SET title = ?, ap_link = ?, created_at = ?, section = ? WHERE id = ?", (title, link, pub_date_str, section, row[0]))
        else:
            c.execute('''INSERT INTO content_items 
                         (section, title, short_desc, image_filename, ap_link, created_at)
                         VALUES (?, ?, ?, ?, ?, ?)''', 
                      (section, title, short_desc, thumbnail, link, pub_date_str))

    conn.commit()
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

with open("templates/index.html", "r") as f:
    content = f.read()

content = content.replace(
    '<section id="highlights" class="section highlights-section">\n            <div class="header-titles"',
    '<section id="highlights" class="section highlights-section">\n            <div class="section-header">\n                <div class="header-titles"'
)

content = content.replace(
    '<section id="reviews" class="section reviews-section">\n            <div class="header-titles"',
    '<section id="reviews" class="section reviews-section">\n            <div class="section-header">\n                <div class="header-titles"'
)

content = content.replace(
    '<section id="news" class="section news-section">\n            <div class="header-titles"',
    '<section id="news" class="section news-section">\n            <div class="section-header">\n                <div class="header-titles"'
)

content = content.replace(
    '<section id="agenda" class="section highlights-section" style="background: #111;">\n            <div class="header-titles"',
    '<section id="agenda" class="section highlights-section" style="background: #111;">\n            <div class="section-header">\n                <div class="header-titles"'
)

with open("templates/index.html", "w") as f:
    f.write(content)

print("Margins fixed.")

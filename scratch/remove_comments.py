import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Quitar split-layout
content = content.replace('split-layout', '')

# Usar regex para quitar los modal-comments-pane
# Busca <div class="modal-comments-pane"> ... </div> (hasta que haya otro div del mismo nivel, o sea </div> del parent).
# Dado que es HTML y regex es limitado, buscaremos exactamente la estructura porque siempre termina en:
# </form></div></div> (cierra modal-comments-pane)
# El final siempre es:
#                         <button type="submit" class="comment-submit-btn">Publicar</button>
#                     </form>
#                 </div>
#             </div>
import re
pattern = re.compile(r'<div class="modal-comments-pane">.*?<button type="submit" class="comment-submit-btn">Publicar</button>\s*</form>\s*</div>\s*</div>', re.DOTALL)

new_content = pattern.sub('', content)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

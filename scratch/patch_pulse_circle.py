with open('app.py', 'r') as f:
    content = f.read()

old_td = '''                        <td bgcolor="#716d4a" style="background-color: #716d4a !important; color: #ffffff !important; font-weight: 900; width: 26px; height: 26px; text-align: center; border-radius: 50%; font-size: 12px; padding: 0;">
                            {idx + 1}
                        </td>'''

new_td = '''                        <td width="26" valign="top" style="padding-top: 3px;">
                            <div style="background-color: #716d4a !important; color: #ffffff !important; font-weight: 900; width: 26px; height: 26px; line-height: 26px; text-align: center; border-radius: 50%; font-size: 12px; margin: 0;">
                                {idx + 1}
                            </div>
                        </td>'''

content = content.replace(old_td, new_td)

with open('app.py', 'w') as f:
    f.write(content)

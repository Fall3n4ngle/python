import cgi
import html
import cgitb
import http.cookies
import os

cgitb.enable()

form = cgi.FieldStorage()

cookies = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
form_count = int(cookies.get("form_count", 0).value)

try:
    q1 = form.getfirst("q1", "Немає відповіді")
    q2 = form.getfirst("q2", "Немає відповіді")

    q3 = form.getfirst("q3", "Немає відповіді")
    q3 = html.escape(q3)

    q4_list = form.getlist("q4")

    if "Рим" in q4_list and "Лондон" in q4_list:
        capitals_message = "Рим і Лондон є столицями країн."
    else:
        capitals_message = "Рим і Лондон не є столицями країн."

    form_count += 1

    cookies["form_count"] = form_count

except (NameError, KeyError) as e:
    message = "Введіть дані для форми"
    print(message)
else:
    message = "Форму оброблено успішно"

print("Content-type:text/html\r\n")
print(cookies.output())  

template_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Обробка форми</title>
</head>
<body>
    <h1>Index html</h1>
    <h2>Ваші відповіді:</h2>
    <p>1. Назвіть будь-яке місто в Японії: {q1}</p>
    <p>2. Назвіть будь-яку країну в Африці: {q2}</p>
    <p>3. Яке місто вважається "Вічним містом"? {q3}</p>
    <p>4. Які з наступних міст є столицями країн?</p>
    <ul>
        <li>Лондон: {'Так' if 'Лондон' in q4_list else 'Ні'}</li>
        <li>Сідней: {'Так' if 'Сідней' in q4_list else 'Ні'}</li>
        <li>Токіо: {'Так' if 'Токіо' in q4_list else 'Ні'}</li>
        <li>Оттава: {'Так' if 'Оттава' in q4_list else 'Ні'}</li>
    </ul>
    <p>{capitals_message}</p>
    <p>Кількість заповнених форм: {form_count}</p>
    <form action="/cgi-bin/form_handler.py" method="post">
        <input type="submit" value="Видалити всі cookies" name="delete_cookies">
    </form>
</body>
</html>
"""

print(template_html)
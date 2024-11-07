<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <title>Portic Map</title>
    <style>
        body {
            background-color: #f0f8ff; /* Light blue background */
            text-align: center; /* Center text */
            font-family: Arial, sans-serif;
        }
        h1, h2 {
            margin: 20px;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        select, button {
            margin: 10px;
            padding: 5px;
            font-size: 16px;
        }
        table {
            margin: auto;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Avec l'API Portic</h1>
        <h2>La carte</h2>
        {{ msg | safe }}

        <h2>Choisissez un pays</h2>
        <form action="/map_template" method="get">
            <select name="pays">
                {% for country in unique_countries %}
                    <option value="{{ country }}">{{ country }}</option>
                {% endfor %}
            </select>
            <button type="submit">Voir la carte</button>
        </form>

        <h2>Les données</h2>
        {{ y | safe }}
    </div>
</body>
</html>

#! /bin/bash
echo "*****Startup script *****"
sudo apt-get update
sudo apt-get install apache2 -y
echo "
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Web Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            text-align: center;
        }
        header {
            background-color: #081427;
            color: white;
            padding: 1em 0;
        }
        .message {
            margin-top: 20px;
            font-size: 1.5em;
        }
    </style>
</head>
<body>
    <header>
        <h1>Welcome to TechTrapture</h1>
    </header>
    <div class="message">
        <p>Hello from $(hostname -f)</p>
    </div>
</body>
</html>
" | sudo tee /var/www/html/index.html
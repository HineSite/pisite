<!DOCTYPE html>
<html lang="en">
<head>
    <?php include __DIR__."/PageParts/MainTheme/Head.php" ?>

    <title>Light Dashboard</title>
</head>
<body class="light-dashboard">
<?php include __DIR__."/PageParts/MainTheme/Header.php" ?>


<div class="dashboard">
    <?php
        $ids = [6,7,20,21,34,35,48,5,8,19,22,33,36,47,4,9,18,23,32,37,46,3,10,17,24,31,38,45,2,11,16,25,30,39,44,1,12,15,26,29,40,43,0,13,14,27,28,41,42];
        for ($i = 0; $i < 49; $i++) {
    ?>

        <div class="light" data-id="<?=$ids[$i]; ?>"></div>
    <?php } ?>
</div>

<div class="buttons">
    <button class="btn" onclick="clearDashboard()">Clear</button>
    <button class="btn" onclick="randomizeDashboard()">Randomize</button>
</div>


<a href="/ControlPanel.php">Control Panel</a>


<?php include __DIR__."/PageParts/MainTheme/Footer.php" ?>

<script type="text/javascript">//<![CDATA[
    const leds = [];
    let spammer = false;

    // Build default led state array
    $('.dashboard .light').each(function (i) {
        let id = $(this).data('id');
        leds.push({
            id: id,
            color: [0,0,0]
        });
    });

    // Set the default state on load
    sendState();
    function sendState() {
        if (spammer) {
            return;
        }

        spammer = true;
        $.ajax({
            url: '/App/Light.php?action=update&leds=' + JSON.stringify(leds),
            type: 'GET',
            success: function(res) {
                for (const led of leds) {
                    $(`[data-id='${led.id}'`).css('background-color', `rgb(${led.color[0]}, ${led.color[1]}, ${led.color[2]})`);
                }

                setTimeout(() => {
                    spammer = false;
                }, 500);
            }
        });
    }

    $('.dashboard .light').click(function (e) {
        let light = $(this);
        let id = light.data('id');

        let hex = prompt('What is your Hex?');
        if (hex != null) {
            let rgb = hexToRGB(hex);
            if (rgb == null) {
                alert('Invalid Hex (e.g. #C7DAD7)')

                return;
            }

            for (const led of leds) {
                if (led.id === id) {
                    led.color = rgb;
                    break;
                }
            }

            sendState();
        }
    });

    function clearDashboard() {
        for (const led of leds) {
            led.color = [0,0,0]
        }

        sendState();
    }

    function randomizeDashboard() {
        for (const led of leds) {
            led.color = getRandoRgb();
        }

        sendState();
    }

    function getRandoRgb() {
        return [
            getRando(0, 255),
            getRando(0, 255),
            getRando(0, 255)
        ];
    }

    function getRando(min, max) {
        return Math.floor(Math.random() * (max - min) + min);
    }

    function hexToRGB(hex) {
        hex = hex.trim('#');

        if (hex.length === 6) {
            let r = parseInt(hex.substr(0, 2), 16);
            let g = parseInt(hex.substr(2, 2), 16);
            let b = parseInt(hex.substr(4, 2), 16);

            return [r, g, b];
        }
        else if (hex.length === 3) {
            let r = parseInt(hex[0] + '' + hex[0], 16);
            let g = parseInt(hex[1] + '' + hex[1], 16);
            let b = parseInt(hex[2] + '' + hex[2], 16);

            return [r, g, b];
        }

        return null;
    }

//]]></script>
</body>
</html>

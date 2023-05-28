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


<div class="links">
    <a href="/ControlPanel.php">Control Panel</a>
    <a href="/editor/">Editor</a>
</div>


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
            url: './App/Light.php?action=update&leds=' + JSON.stringify(leds),
            type: 'GET',
            success: function(res) {
                for (const led of leds) {
                    $(`[data-id='${led.id}']`).css('background-color', `rgb(${led.color[0]}, ${led.color[1]}, ${led.color[2]})`);
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
        hex = hex.replace('#', '').replace(' ', '');

        let namedColor = colorNameToHex(hex);
        if (namedColor) {
            hex = namedColor;
        }

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

    function colorNameToHex(color)
    {
        var colors = {
            "aliceblue":"f0f8ff","antiquewhite":"faebd7","aqua":"00ffff","aquamarine":"7fffd4","azure":"f0ffff",
            "beige":"f5f5dc","bisque":"ffe4c4","black":"000000","blanchedalmond":"ffebcd","blue":"0000ff","blueviolet":"8a2be2","brown":"a52a2a","burlywood":"deb887",
            "cadetblue":"5f9ea0","chartreuse":"7fff00","chocolate":"d2691e","coral":"ff7f50","cornflowerblue":"6495ed","cornsilk":"fff8dc","crimson":"dc143c","cyan":"00ffff",
            "darkblue":"00008b","darkcyan":"008b8b","darkgoldenrod":"b8860b","darkgray":"a9a9a9","darkgreen":"006400","darkkhaki":"bdb76b","darkmagenta":"8b008b","darkolivegreen":"556b2f",
            "darkorange":"ff8c00","darkorchid":"9932cc","darkred":"8b0000","darksalmon":"e9967a","darkseagreen":"8fbc8f","darkslateblue":"483d8b","darkslategray":"2f4f4f","darkturquoise":"00ced1",
            "darkviolet":"9400d3","deeppink":"ff1493","deepskyblue":"00bfff","dimgray":"696969","dodgerblue":"1e90ff",
            "firebrick":"b22222","floralwhite":"fffaf0","forestgreen":"228b22","fuchsia":"ff00ff",
            "gainsboro":"dcdcdc","ghostwhite":"f8f8ff","gold":"ffd700","goldenrod":"daa520","gray":"808080","green":"008000","greenyellow":"adff2f",
            "honeydew":"f0fff0","hotpink":"ff69b4",
            "indianred ":"cd5c5c","indigo":"4b0082","ivory":"fffff0","khaki":"f0e68c",
            "lavender":"e6e6fa","lavenderblush":"fff0f5","lawngreen":"7cfc00","lemonchiffon":"fffacd","lightblue":"add8e6","lightcoral":"f08080","lightcyan":"e0ffff","lightgoldenrodyellow":"fafad2",
            "lightgrey":"d3d3d3","lightgreen":"90ee90","lightpink":"ffb6c1","lightsalmon":"ffa07a","lightseagreen":"20b2aa","lightskyblue":"87cefa","lightslategray":"778899","lightsteelblue":"b0c4de",
            "lightyellow":"ffffe0","lime":"00ff00","limegreen":"32cd32","linen":"faf0e6",
            "magenta":"ff00ff","maroon":"800000","mediumaquamarine":"66cdaa","mediumblue":"0000cd","mediumorchid":"ba55d3","mediumpurple":"9370d8","mediumseagreen":"3cb371","mediumslateblue":"7b68ee",
            "mediumspringgreen":"00fa9a","mediumturquoise":"48d1cc","mediumvioletred":"c71585","midnightblue":"191970","mintcream":"f5fffa","mistyrose":"ffe4e1","moccasin":"ffe4b5",
            "navajowhite":"ffdead","navy":"000080",
            "oldlace":"fdf5e6","olive":"808000","olivedrab":"6b8e23","orange":"ffa500","orangered":"ff4500","orchid":"da70d6",
            "palegoldenrod":"eee8aa","palegreen":"98fb98","paleturquoise":"afeeee","palevioletred":"d87093","papayawhip":"ffefd5","peachpuff":"ffdab9","peru":"cd853f","pink":"ffc0cb","plum":"dda0dd","powderblue":"b0e0e6","purple":"800080",
            "rebeccapurple":"663399","red":"ff0000","rosybrown":"bc8f8f","royalblue":"4169e1",
            "saddlebrown":"8b4513","salmon":"fa8072","sandybrown":"f4a460","seagreen":"2e8b57","seashell":"fff5ee","sienna":"a0522d","silver":"c0c0c0","skyblue":"87ceeb","slateblue":"6a5acd","slategray":"708090","snow":"fffafa","springgreen":"00ff7f","steelblue":"4682b4",
            "tan":"d2b48c","teal":"008080","thistle":"d8bfd8","tomato":"ff6347","turquoise":"40e0d0",
            "violet":"ee82ee",
            "wheat":"f5deb3","white":"ffffff","whitesmoke":"f5f5f5",
            "yellow":"ffff00","yellowgreen":"9acd32"
        };

        if (typeof colors[color.toLowerCase()] != 'undefined')
            return colors[color.toLowerCase()];

        return false;
    }

//]]></script>
</body>
</html>

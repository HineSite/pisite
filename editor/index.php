<?php include __DIR__."/api/editor.php" ?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>PyPy Editor</title>

    <link rel="stylesheet" type="text/css" href="/resources/css/editor.css" />
    <link rel="stylesheet" href="https://code.jquery.com/ui/1.13.2/themes/base/jquery-ui.css"/>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ace-builds@1.15.1/css/ace.min.css">
</head>
<body class="editor">
<div class="top">
    <div class="controls">
        <div class="buttons">
            <button class="btn" onclick="saveScript(this)">Save</button>
            <button class="btn" onclick="runScript(this)">Run</button>
            <input id="filenameField" type="text" placeholder="filename">
        </div>

        <div class="files">
            <?php
            $first = true;
            foreach (getScripts() as $script) {
                echo '<div onclick="openScript(this)" class="file" data-filename="' . $script . '">' . trim($script, '.py') . '</div>';

                $first = false;
            }
            ?>
        </div>
    </div>

    <div id="editor"></div>
</div>


<div class="middle-bar">
    <div class="tab terminal" onclick="toggleTerminal()">Terminal</div>
</div>

<div class="terminal-wrapper">
    <div id="terminal" class="terminal"></div>
</div>

<script type="application/javascript" src=""></script>
<script src="https://code.jquery.com/jquery-3.6.3.min.js"></script>
<script src="https://code.jquery.com/ui/1.13.2/jquery-ui.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/ace-builds@1.15.1/src-min-noconflict/ace.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/ace-builds@1.15.1/src-min-noconflict/mode-python.js"></script>
<script type="text/javascript">//<![CDATA[
    $('.controls').resizable({
        handles: 'e',
        minWidth: 100
    });

    /*$('.terminal').resizable({
      handles: 'n',
          minWidth: 100,
      maxWidth: 400
    });*/


    var mode = ace.require("ace/mode/python").Mode;

    var editor = ace.edit("editor");
    editor.session.setMode(new mode());







    let spammer = false;


    function openScript(e) {
        if (spammer) {
            return;
        }

        let me = $(e);
        let filename = me.data('filename');

        spammer = true;
        $.ajax({
            url: '/editor/api/editor.php?action=getScript&file=' + filename,
            type: 'GET',
            success: function(res) {
                editor.session.setValue(res, -1);
                $("#filenameField").val(filename);
                $('.controls .files .file').removeClass('active');
                me.addClass('active');

                setTimeout(() => {
                    spammer = false;
                }, 500);
            }
        });
    }


    function saveScript(e) {
        if (spammer) {
            return;
        }

        spammer = true;
        $.ajax({
            url: '/editor/api/editor.php?action=saveScript&file=' + $("#filenameField").val(),
            type: 'POST',
            data: editor.getValue(),
            dataType: 'text',
            success: function(res) {

                setTimeout(() => {
                    spammer = false;
                }, 500);
            }
        });
    }


    function runScript(e) {
        if (spammer) {
            return;
        }

        spammer = true;
        $.ajax({
            url: '/editor/api/editor.php?action=runScript&file=' + $("#filenameField").val(),
            type: 'POST',
            data: editor.getValue(),
            dataType: 'text',
            success: function(res) {
                let terminal = $('#terminal');
                let time = (new Date()).toLocaleTimeString();

                try {
                    let json = JSON.parse(res);
                    if (json.stdout) {
                        terminal.append('<div class="stdout"><span class="time">'+ time + ':</span> ' + json.stdout.replaceAll('\n', '<br>') + '</div>');
                    }

                    if (json.stderr) {
                        terminal.append('<div class="stderr"><span class="time">'+ time + ':</span> ' + json.stderr.replaceAll('\n', '<br>') + '</div>');
                    }
                }
                catch {
                    terminal.append('<div class="error"><span class="time">'+ time + ':</span> ' + res + '</div>');
                }

                if (terminal.parent().scrollTop() > -150) {
                    terminal.parent().scrollTop(0);
                }

                setTimeout(() => {
                    spammer = false;
                }, 500);
            }
        });
    }

    function toggleTerminal() {
        $(".terminal-wrapper").slideToggle();
    }


    $('.controls .files .file').first().click();

    document.addEventListener('keydown', e => {
        if (e.ctrlKey && e.key === 's') {
            // Prevent the Save dialog to open
            e.preventDefault();

            saveScript();
        }
    });
//]]></script>
</body>
</html>

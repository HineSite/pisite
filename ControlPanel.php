<!DOCTYPE html>
<html lang="en">
<head>
    <?php include __DIR__."/PageParts/MainTheme/Head.php" ?>

    <title>Control Panel</title>
</head>
<body>
<?php include __DIR__."/PageParts/MainTheme/Header.php" ?>


<div class="inline-forms">
    <form action="/App/Control.php" method="post">
        <input type="hidden" name="SubmitAction" value="restart">
        <input class="btn" type="submit" value="Restart">
    </form>

    <form action="/App/Control.php" method="post">
        <input type="hidden" name="SubmitAction" value="shutdown">
        <input class="btn" type="submit" value="Shutdown">
    </form>
</div>


<?php include __DIR__."/PageParts/MainTheme/Footer.php" ?>
</body>
</html>

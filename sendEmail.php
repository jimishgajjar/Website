<?php
// if (isset($_POST['contact-submit'])) {
if (isset($_POST["name"]) && isset($_POST["email"]) && isset($_POST["comments"]) && isset($_POST["subject"])) {
    $name = htmlspecialchars(stripslashes(trim($_POST['name'])));
    $subject = htmlspecialchars(stripslashes(trim($_POST['subject'])));
    $email = htmlspecialchars(stripslashes(trim($_POST['email'])));
    $comments = htmlspecialchars(stripslashes(trim($_POST['comments'])));

    if (!preg_match("/^[A-Za-z .'-]+$/", $name)) {
        echo 'Invalid name';
    } else if (!preg_match("/^[A-Za-z .'-]+$/", $subject)) {
        echo 'Invalid subject';
    } else if (!preg_match("/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/", $email)) {
        echo 'Invalid email';
    } else if (strlen($comments) === 0) {
        echo 'Your comments should not be empty';
    } else {
        $txt = "\nName = " . $name . "\nEmail = " . $email . "\nSubject = " . $subject . "\nMessage = " . $comments;
        if (mail("jimish.gajjar@gmail.com", $name . " is intrested to your service.\n", $txt)) {
            echo 'Congratulation';
        } else {
            echo 'not success';
        }
    }
}
// }

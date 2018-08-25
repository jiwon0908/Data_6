<?php

if(!$_POST) exit;

// Email verification, do not edit.
function isEmail($email_newsletter ) {
	return(preg_match("/^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$/",$email_newsletter ));
}

if (!defined("PHP_EOL")) define("PHP_EOL", "\r\n");

$email_newsletter_2    = $_POST['email_newsletter'];

if(trim($email_newsletter_2) == '') {
	echo '<div class="error_message">올바른 이메일 주소를 입력해주세요.</div>';
	exit();
}
//$address = "your email address";
$address = "korra0501@gmail.com";

// Below the subject of the email
$e_subject = '동행 - 새로운 구독 요청';

// You can change this if you feel that you need to.
$e_body = "$email_newsletter 님께서 구독을 원하십니다." . PHP_EOL . PHP_EOL;
$e_content = "\"$email_newsletter\"" . PHP_EOL . PHP_EOL;

$msg = wordwrap( $e_body . $e_content, 70 );

$headers = "From: $email_newsletter" . PHP_EOL;
$headers .= "Reply-To: $email_newsletter" . PHP_EOL;
$headers .= "MIME-Version: 1.0" . PHP_EOL;
$headers .= "Content-type: text/plain; charset=utf-8" . PHP_EOL;
$headers .= "Content-Transfer-Encoding: quoted-printable" . PHP_EOL;

$user = "$email_newsletter";
$usersubject = "동행 - 구독해 주셔서 감사합니다.";
$userheaders = "From: korra0501@gmail.com\n";
$usermessage = "동행의 새로운 소식을 구독해주셔서 감사합니다! 여러분의 동행자가 되어드리겠습니다.";
mail($user,$usersubject,$usermessage,$userheaders);

if(mail($address, $e_subject, $msg, $headers)) {

	// Success message
	echo "<div id='success_page' style='padding-top:11px'>";
	echo "감사합니다, <strong>$email_newsletter</strong>님. 구독 신청이 완료되었습니다!!";
	echo "</div>";

} else {

	echo '오류!';

}
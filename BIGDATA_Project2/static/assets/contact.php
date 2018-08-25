<?php

if(!$_POST) exit;

// Email verification, do not edit.
function isEmail($email_contact ) {
	return(preg_match("/^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$/",$email_contact ));
}

if (!defined("PHP_EOL")) define("PHP_EOL", "\r\n");

$name_contact     = $_POST['name_contact'];
$lastname_contact    = $_POST['lastname_contact'];
$email_contact    = $_POST['email_contact'];
$phone_contact   = $_POST['phone_contact'];
$message_contact = $_POST['message_contact'];
$verify_contact   = $_POST['verify_contact'];

if(trim($name_contact) == '') {
	echo '<div class="error_message">성을 입력해야 합니다.</div>';
	exit();
} else if(trim($lastname_contact ) == '') {
	echo '<div class="error_message">이름을 입력해야 합니다.</div>';
	exit();
} else if(trim($email_contact) == '') {
	echo '<div class="error_message">유효한 이메일 주소를 입력해주세요.</div>';
	exit();
} else if(!isEmail($email_contact)) {
	echo '<div class="error_message">유효하지 않은 이메일 주소를 입력하셨습니다. 다시 시도해주세요.</div>';
	exit();
	} else if(trim($phone_contact) == '') {
	echo '<div class="error_message">유효한 전화번호를 입력해주세요.</div>';
	exit();
} else if(!is_numeric($phone_contact)) {
	echo '<div class="error_message">전화번호는 숫자만 포함해야 합니다.</div>';
	exit();
} else if(trim($message_contact) == '') {
	echo '<div class="error_message">메세지를 입력해주세요.</div>';
	exit();
} else if(!isset($verify_contact) || trim($verify_contact) == '') {
	echo '<div class="error_message"> 인증 숫자를 입력해주세요.</div>';
	exit();
} else if(trim($verify_contact) != '5') {
	echo '<div class="error_message">입력하신 인증 숫자가 정확하지 않습니다.</div>';
	exit();
}

if(get_magic_quotes_gpc()) {
	$message_contact = stripslashes($message_contact);
}


//$address = "HERE your email address";
$address = "korra0501@gmail.com";


// Below the subject of the email
$e_subject = '동행 - You\'ve been contacted by ' . $name_contact . '.';

// You can change this if you feel that you need to.
$e_body = "$name_contact $lastname_contact 님이 다음과 같은 메세지를 보내셨습니다." . PHP_EOL . PHP_EOL;
$e_content = "\"$message_contact\"" . PHP_EOL . PHP_EOL;
$e_reply = "You can contact $lastname_contact via email, $email_contact or via phone $phone_contact";

$msg = wordwrap( $e_body . $e_content . $e_reply, 70 );

$headers = "From: $email_contact" . PHP_EOL;
$headers .= "Reply-To: $email_contact" . PHP_EOL;
$headers .= "MIME-Version: 1.0" . PHP_EOL;
$headers .= "Content-type: text/plain; charset=utf-8" . PHP_EOL;
$headers .= "Content-Transfer-Encoding: quoted-printable" . PHP_EOL;

$user = "$email_contact";
$usersubject = "감사합니다";
$userheaders = "From: korra0501@gmail.com\n";
$usermessage = "동행에 문의를 넣어주셔서 감사합니다. 답장이 올 때까지 조금만 기다려주세요!";
mail($user,$usersubject,$usermessage,$userheaders);

if(mail($address, $e_subject, $msg, $headers)) {

	// Success message
	echo "<div id='success_page' style='padding:25px 0'>";
	echo "<strong >이메일 전송 완료.</strong><br>";
	echo "<strong>$name_contact</strong>님 감사합니다.<br> 문의가 접수 완료되었습니다. 가까운 시일 안에 답장드리겠습니다.";
	echo "</div>";

} else {

	echo 'ERROR!';

}

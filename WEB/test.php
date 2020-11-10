<?php
$servername = "119.3.223.214";
$username = "root";
$password = "sigh987yu";
$dbname = "MAKARA";

// 创建连接
$conn = mysqli_connect($servername, $username, $password, $dbname);
// Check connection
if (!$conn) {
	die("连接失败: " . mysqli_connect_error());
}
mysqli_close($conn);
?>
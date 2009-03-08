<%@ page contentType="text/html;charset=UTF-8" language="java" isELIgnored="false" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<html>
<head><title>DreamboxMessageServer - send message</title></head>
<body>
	<a href="index.html">index</a>
	<h1>Send a message to dreambox</h1>
	<form action="DreamboxMessageServer" method="post">
		<input name="action" value="message" type="hidden">
		<table border="0" cellpadding="0" cellspacing="4">
			<tr>
				<td align="right">Password:</td>
				<td>
					<input name="password" type="password" maxlength="30" value="${password}">
					<c:if test="${passwordMissing}"><span style="color: red;">missing</span></c:if>
				</td>
			</tr>
			<tr>
				<td align="right">Message:</td>
				<td>
					<textarea name="message" cols="50" rows="10">${message}</textarea>
					<c:if test="${messageMissing}"><span style="color: red;">missing</span></c:if>
				</td>
			</tr>
			<tr>
				<td></td>
				<td><input type="submit" value="send message"></td>
			</tr>
		</table>
		<c:if test="${error != null}"><span style="color: red;">${error}</span></c:if>
		<c:if test="${status != null}"><span style="color: green;">${status}</span></c:if>
	</form>
</body>
</html>
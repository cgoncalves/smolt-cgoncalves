<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Show Box</title>
${ratingwidget.display(update="rating", 
                       href="/client/rate_object", 
                       num="5",
                       img_on="/static/images/stars/rating_on.gif",
                       img_off="/static/images/stars/rating_off.gif",
                       img_over="/static/images/stars/rating_over.gif",
                       imgon_pre="/static/images/rating/r",
                       imgoff_pre="/static/images/rating/ro",
                       imgbusy_pre="/static/images/rating/rb",
                       img_post=".png",
)}
</head>
<body>
<!--
	<div class='share' id='share' name='share'>
		<a href='/client/share?sid=${host_object.id}'>Share my computer!</a>
	</div>
-->
        <h3>${host_object.pub_uuid}</h3>

	<div id="legend">
	    <img src="/static/images/rating/r0.png"/> I don't use this/I don't know<br/>
	    <img src="/static/images/rating/r1.png"/> Breaks System<br/>
	    <img src="/static/images/rating/r2.png"/> Doesn't Work<br/>
	    <img src="/static/images/rating/r3.png"/> Requires 3rd Party Drivers<br/>
	    <img src="/static/images/rating/r4.png"/> Works, but required aditional configuration<br/>
	    <img src="/static/images/rating/r5.png"/> Worked out of the box<br/>
	    <p><a href="/client/show_all?uuid=${host_object.pub_uuid}">Show all Information</a></p>
	</div>
        <table id="system_show">
       	    <tr><th>Overall Rating:</th><td><div class="rating" id="Host${host_object.pub_uuid}">${host_object.rating}</div></td></tr>
            <tr><th>UUID:</th><td>${host_object.pub_uuid}</td></tr>
            <tr><th>Operating System:</th><td><a href="${getOSWikiLink(host_object.os)}">${host_object.os}</a></td></tr>
            <tr><th>Platform:</th><td>${host_object.platform}</td></tr>
            <tr><th>System Vendor:</th><td>${host_object.vendor}</td></tr>
            <tr><th>System Model:</th><td><a href="${host_link}">${host_object.system}</a></td></tr>
            <tr><th>Kernel</th><td>${host_object.kernel_version}</td></tr>
            <tr><th>Formfactor</th><td>${host_object.formfactor}</td></tr>
            <tr><th>Last Modified</th><td>${host_object.last_modified}</td></tr>
        </table> 
        <h3>Devices</h3>
        <table id="device_show">
            <tr>
                <th>Rating</th><th>Device</th><th>Class</th>
            </tr>
            <tr py:for='device in devices'>
            	<td><div class="rating" id="Host${host_object.pub_uuid}@Device${device.get('id')}">${device.get('rating')}</div></td>
		<td><a href="${device.get('link')}">${device.get('name')}</a></td>
                <td align='center'>${device.get('cls')}</td>
            </tr>
        </table>
</body>
</html>

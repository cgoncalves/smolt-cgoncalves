<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Show Box</title>
${ratingwidget.display(update="rating", 
                       href="/rate_object", 
                       num="5",
                       img_on="/static/images/stars/rating_on.gif",
                       img_off="/static/images/stars/rating_off.gif",
                       img_over="/static/images/stars/rating_over.gif",
                       imgon_pre="/static/images/rating/r",
                       imgoff_pre="/static/images/rating/ro",
                       img_post=".gif",
)}
</head>
<body>

<span py:def="wikilink(bus, vendor_id, device_id, subsys_vendor_id, subsys_device_id)">
<a py:if="bus and vendor_id and device_id" href="${getWikiLink(bus, vendor_id, device_id, subsys_vendor_id, subsys_device_id)}">[Wiki]</a>&nbsp;
</span>

	<div class='share' id='share' name='share'>
		<a href='share?sid=${host_object.id}'>Share my computer!</a>
	</div>
        <h3>${host_object.uuid}</h3>

	<div id="legend">
	    <img src="/static/images/rating/r1.gif"/> Breaks System<br/>
	    <img src="/static/images/rating/r2.gif"/> Doesn't Work<br/>
	    <img src="/static/images/rating/r3.gif"/> Requires 3rd Party Drivers<br/>
	    <img src="/static/images/rating/r4.gif"/> Works, but required aditional configuration<br/>
	    <img src="/static/images/rating/r5.gif"/> Worked out of the box<br/>
	</div>
        <table id="show">
       	    <tr><th>Rating:</th><td><div class="rating" id="Host${host_object.uuid}">${host_object.rating}</div></td></tr>
            <tr><th>UUID:</th><td>${host_object.uuid}</td></tr>
            <tr><th>Operating System:</th><td>${host_object.os}</td></tr>
            <tr><th>Platform:</th><td>${host_object.platform}</td></tr>
            <tr><th>Bogomips:</th><td>${host_object.bogomips}</td></tr>
            <tr><th>CPU Speed:</th><td>${host_object.cpu_speed}</td></tr>
            <tr><th>System Memory:</th><td>${host_object.system_memory}</td></tr>
            <tr><th>CPUVendor:</th><td>${host_object.cpu_vendor}</td></tr>
            <tr><th>Number of CPUs:</th><td>${host_object.num_cpus}</td></tr>
            <tr><th>Language:</th><td>${host_object.language}</td></tr>
            <tr><th>Default Runlevel:</th><td>${host_object.default_runlevel}</td></tr>
            <tr><th>System Vendor:</th><td>${host_object.vendor}</td></tr>
            <tr><th>System Model:</th><td>${host_object.system}</td></tr>
            <tr><th>Kernel</th><td>${host_object.kernel_version}</td></tr>
            <tr><th>Formfactor</th><td>${host_object.formfactor}</td></tr>
            <tr><th>SELinux Enabled</th><td>${host_object.selinux_enabled}</td></tr>
            <tr><th>SELinux Enforce</th><td>${host_object.selinux_enforce}</td></tr>
            <tr><th>Last Modified</th><td>${host_object.last_modified}</td></tr>
        </table> 
        <h3>Devices</h3>
        <table id='show'>
            <tr>
                <th>Rating</th><th align='right'>Driver</th><th>Class</th><th>Bus</th><th>Vendor</th><th>Device</th><th>SubVendor</th><th>SubDevice</th><th>Wiki</th>
            </tr>
            <tr py:for='device_node in devices.values()'>
            	<?python device = device_node[0] ?>
            	<td align='left'><div class="rating" id="Host${host_object.uuid}_Device${device.id}">${device_node[1]}</div></td>
                <td align='right'>${device.driver}</td>
                <td align='center'>${device.cls}</td>
                <td align='center'>${device.bus}</td>
                <td align='center'>${ven.vendor(device.vendor_id, bus=device.bus)}</td>
                <td align='center'>${ven.device(device.vendor_id, device.device_id, alt=device.description, bus=device.bus)}</td>
                <td align='center'>${ven.vendor(device.subsys_device_id)}</td>
                <td align='center'>${ven.subdevice(device.vendor_id, device.device_id, device.subsys_vendor_id, device.subsys_device_id)}</td>
		<td align='center'><span py:replace="wikilink(device.bus, device.vendor_id, device.device_id, device.subsys_vendor_id, device.subsys_device_id)">Wiki</span></td>
                <!--<td align='left'>${device.Description}</td>-->
            </tr>
        </table>
</body>
</html>

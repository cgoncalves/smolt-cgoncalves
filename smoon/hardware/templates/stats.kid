<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title> Stats </title>
</head>
<body>
    <table id="stats" width="100%" border="0" cellpadding="3" cellspacing="3">
        <tr>
            <th valign="top" width="25%">Total Registered Hosts</th>
            <td><strong>${stat['total_hosts']}</strong></td>
        </tr>
        <tr>
            <th valign="top">Total Registered Devices</th>
            <td><strong>${stat['registered_devices']}</strong></td>
        </tr>
        <tr>
            <th valign="top">Total bogomips</th>
            <td><strong>${stat["bogomips_total"]}</strong></td>
        </tr>
        <tr>
            <th valign="top">Total processors</th>
            <td><strong>${stat["cpus_total"]}</strong></td>
        </tr>
        <tr>
            <th valign="top">Total MHz</th>
            <td><strong>${stat["cpu_speed_total"]}</strong></td>
        </tr>
    </table>
    <div class="tabber">
        <div class="tabbertab"><h2>Archs</h2>
            <table id="stats" width="100%" border="0" cellpadding="3" cellspacing="3">
                <tr><th>Arch</th><th>Count</th><th>% of total</th><th halign="left"> </th></tr>
                <tr py:for='arch in stat["archs"]'>
                    <th align="right">${arch.platform}</th>
                    <td align="center">${arch.cnt}</td>
                    <td><strong>${'%.1f' % (float(arch.cnt) / total_hosts * 100) } %</strong></td>
                    <td><table border='0' cellpadding='0' cellspacing='0'><tr><td width='${ float(arch.cnt) / total_hosts * 100 }'><div width='100%' id="bar"></div></td><td width='${ 100 - (float(arch.cnt) / total_hosts * 100) }'></td></tr></table></td>
                </tr>
            </table>
        </div>
        <div class="tabbertab"><h2>OS</h2>
            <table id="stats" width="100%" border="0" cellpadding="3" cellspacing="3">
                <tr py:for='OS in stat["os"]'>
                    <th align="right">${OS.os}</th>
                    <td align="center">${OS.cnt}</td>
                    <td><strong>${'%.1f' % (float(OS.cnt) / total_hosts * 100) } %</strong></td>
                    <td><table border='0' cellpadding='0' cellspacing='0'><tr><td width='${ float(OS.cnt) / total_hosts * 100 }'><div id="bar"></div></td><td></td></tr></table></td>
                </tr>
            </table>
        </div>
        <div class="tabbertab"><h2>Runlevel</h2>
            <table id="stats" width="100%" border="0" cellpadding="3" cellspacing="3">
                <tr py:for='rl in stat["runlevel"]'>
                    <th align="right">${rl.runlevel}</th>
                    <td align="center">${rl.cnt}</td>
                    <td><strong>${'%.1f' % (float(rl.cnt) / total_hosts * 100) } %</strong></td>
                    <td><table border='0' cellpadding='0' cellspacing='0'><tr><td width='${ float(rl.cnt) / total_hosts * 100 }'><div id="bar"></div></td><td></td></tr></table></td>
                </tr>
            </table>
        </div>
        <div class="tabbertab"><h2>Language</h2>
            <table id="stats" width="100%" border="0" cellpadding="3" cellspacing="3">
                <tr py:for='lang in stat["language"]'>
                    <th align="right">${lang.language}</th>
                    <td align="center">${lang.cnt}</td>
                    <td><strong>${'%.1f' % (float(lang.cnt) / total_hosts * 100) } %</strong></td>
                    <td><table border='0' cellpadding='0' cellspacing='0'><tr><td width='${ float(lang.cnt) / total_hosts * 100 }'><div id="bar"></div></td><td></td></tr></table></td>
                </tr>
            </table>
        </div>
        <div class="tabbertab"><h2>Vendor</h2>
            <table id="stats" width="100%" border="0" cellpadding="3" cellspacing="3">
                <tr py:for='vendor in stat["vendors"]'>
                    <th align="right">${vendor.vendor}</th>
                    <td align="center">${vendor.cnt}</td>
                    <td><strong>${'%.1f' % (float(vendor.cnt) / total_hosts * 100) } %</strong></td>
                    <td><table border='0' cellpadding='0' cellspacing='0'><tr><td width='${ float(vendor.cnt) / total_hosts * 100 }'><div id="bar"></div></td><td></td></tr></table></td>
                </tr>
            </table>
        </div>
        <div class="tabbertab"><h2>Model</h2>
            <table id="stats" width="100%" border="0" cellpadding="3" cellspacing="3">
                <tr py:for='system in stat["systems"]'>
                    <!-- Temporary solution to a silly problem -->
                    <th align="right">${system.system.split(' Not')[0].split(' To be')[0].split('System Version')[0]}</th>
                    <td align="center">${system.cnt}</td>
                    <td><strong>${'%.1f' % (float(system.cnt) / total_hosts * 100) } %</strong></td>
                    <td><table border='0' cellpadding='0' cellspacing='0'><tr><td width='${ float(system.cnt) / total_hosts * 100 }'><div id="bar"></div></td><td></td></tr></table></td>
                </tr>
            </table>
        </div>
        <div class="tabbertab"><h2>RAM</h2>
            <table id="stats" width="100%" border="0" cellpadding="3" cellspacing="3">
                <tr py:for='mem in stat["sys_mem"]'>
                    <th align="right">${mem[0]}</th>
                    <td align="center">${mem[1]}</td>
                    <td><strong>${'%.1f' % (float(mem[1]) / total_hosts * 100) } %</strong></td>
                    <td><table border='0' cellpadding='0' cellspacing='0'><tr><td width='${ float(mem[1]) / total_hosts * 100 }'><div id="bar"></div></td><td></td></tr></table></td>
                </tr>
            </table>
        </div>
        <div class="tabbertab"><h2>Swap</h2>
            <table id="stats" width="100%" border="0" cellpadding="3" cellspacing="3">
                <tr py:for='mem in stat["swap_mem"]'>
                    <th align="right">${mem[0]}</th>
                    <td align="center">${mem[1]}</td>
                    <td><strong>${'%.1f' % (float(mem[1]) / total_hosts * 100) } %</strong></td>
                    <td><table border='0' cellpadding='0' cellspacing='0'><tr><td width='${ float(mem[1]) / total_hosts * 100 }'><div id="bar"></div></td><td></td></tr></table></td>
                </tr>
            </table>
        </div>
        <div class="tabbertab"><h2>CPU</h2>
            <table id="stats" width="100%" border="0" cellpadding="3" cellspacing="3">
                <tr><th colspan="4">Speed (MHz)</th></tr>
                <tr py:for='cpu_speed in stat["cpu_speed"]'>
                    <th align="right">${cpu_speed[0]}</th>
                    <td align="center">${cpu_speed[1]}</td>
                    <td><strong>${'%.1f' % (float(cpu_speed[1]) / total_hosts * 100) } %</strong></td>
                     <td><table border='0' cellpadding='0' cellspacing='0'><tr><td width='${ float(cpu_speed[1]) / total_hosts * 100 }'><div id="bar"></div></td><td></td></tr></table></td>
               </tr>
                <tr><th colspan="4">Number of CPUs</th></tr>
                <tr py:for='num_cpus in stat["num_cpus"]'>
                    <th align="right">${num_cpus.num_cpus}</th>
                    <td align="center">${num_cpus.cnt}</td>
                    <td><strong>${'%.1f' % (float(num_cpus.cnt) / total_hosts * 100) } %</strong></td>
                    <td><table border='0' cellpadding='0' cellspacing='0'><tr><td width='${ float(num_cpus.cnt) / total_hosts * 100 }'><div id="bar"></div></td><td></td></tr></table></td>
                </tr>
                <tr><th colspan="4">CPU Vendor</th></tr>
                <tr py:for='cpu_vendor in stat["cpu_vendor"]'>
                    <th align="right">${cpu_vendor.cpu_vendor}</th>
                    <td align="center">${cpu_vendor.cnt}</td>
                    <td><strong>${'%.1f' % (float(cpu_vendor.cnt) / total_hosts * 100) } %</strong></td>
                    <td><table border='0' cellpadding='0' cellspacing='0'><tr><td width='${ float(cpu_vendor.cnt) / total_hosts * 100 }'><div id="bar"></div></td><td></td></tr></table></td>
                </tr>
                <tr><th colspan="4">Bogomips</th></tr>
                <tr py:for='bogomips in stat["bogomips"]'>
                    <th align="right">${bogomips[0]}</th>
                    <td align="center">${bogomips[1]}</td>
                    <td><strong>${'%.1f' % (float(bogomips[1]) / total_hosts * 100) } %</strong></td>
                    <td><table border='0' cellpadding='0' cellspacing='0'><tr><td width='${ float(bogomips[1]) / total_hosts * 100 }'><div id="bar"></div></td><td></td></tr></table></td>
                </tr>
            </table>
        </div>
        <div class="tabbertab"><h2>Kernel</h2>
            <table id="stats" width="100%" border="0" cellpadding="3" cellspacing="3">
                <tr py:for='kernel_version in stat["kernel_version"]'>
                    <th align="right">${kernel_version.kernel_version}</th>
                    <td align="center">${kernel_version.cnt}</td>
                    <td><strong>${'%.1f' % (float(kernel_version.cnt) / total_hosts * 100) } %</strong></td>
                    <td><table border='0' cellpadding='0' cellspacing='0'><tr><td width='${ float(kernel_version.cnt) / total_hosts * 100 }'><div id="bar"></div></td><td></td></tr></table></td>
                </tr>
            </table>
        </div>
        <div class="tabbertab"><h2>Form Factor</h2>
            <table id="stats" width="100%" border="0" cellpadding="3" cellspacing="3">
                <tr py:for='formfactor in stat["formfactor"]'>
                    <th align="right">${formfactor.formfactor}</th>
                    <td align="center">${formfactor.cnt}</td>
                    <td><strong>${'%.1f' % (float(formfactor.cnt) / total_hosts * 100) } %</strong></td>
                    <td><table border='0' cellpadding='0' cellspacing='0'><tr><td width='${ float(formfactor.cnt) / total_hosts * 100 }'><div id="bar"></div></td><td></td></tr></table></td>
                </tr>
            </table>
        </div>
    </div>

</body>
</html>

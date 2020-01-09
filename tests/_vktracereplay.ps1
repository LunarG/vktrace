# Powershell script for running the vktrace trace/replay auto test
# To run this test:
#    cd <this-dir>
#    ???powershell C:\src\ValidationLayers\vktracereplay.ps1 [-Debug]
#
#    ???<tracepath> example: "C:\trace" would result in the script testing against "C:\trace.vktrace" and "C:\trace.ppm"
param (
    [switch]$Debug
)

if ($Debug) {
    $dPath = "Debug"
} else {
    $dPath = "Release"
}

write-host -background black -foreground green "[  RUN     ] " -nonewline
write-host "_vktracereplay.ps1: Vktrace trace/replay"

& python $PWD\vktracereplay.py $PWD\..\vktrace\$dPath\vktrace.exe $PWD\..\vktrace\$dPath $PWD\..\vktrace\$dPath\vkreplay.exe
if ($LastExitCode -eq 0) {
    $exitstatus = 0
} else {
    echo 'Trace/replay regression tests failed.'
    write-host -background black -foreground red "[  FAILED  ] "  -nonewline;
    $exitstatus = 1
}

# if we passed all the checks, the test is good
if ($exitstatus -eq 0) {
   write-host -background black -foreground green "[  PASSED  ] " -nonewline;
}

write-host "_vktracereplay.ps1: Vktrace trace/replay"
write-host
if ($exitstatus) {
    echo '1 FAILED TEST'
}

exit $exitstatus

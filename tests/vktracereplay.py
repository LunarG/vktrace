# Python script for running the regression test for both trace and replay. Python version 3 or greater required.
# NOTES -
#   vkcube is expected to be in PATH
#   The enviroment variable SCREENSHOT_LAYER_PATH can be set to a dir containing the
#       screenshot layer json and library files. If it is not set, it defaults to:
#       ../../../VulkanTools/build/layersvt (Linux)
#       ../../../VulkanTools/build/layersvt/Debug (Windows)
#   This script is normally invoked from _vktracereplay.ps1 or vktracereplay.sh.
#
# vkcube is traced and replayed with screenshot comparison.
#
# To run this test:
#    cd <this-dir>
#    python ./vktracereplay.py <vktrace-exe> <vktrace-layer-path> <vkreplay-exe>
#

import os, sys, subprocess, time, argparse, filecmp, time, shutil, glob

class VktraceException(Exception):
    pass



def rmfileext(ext):
   # Remove all files in current dir that end with the given extension
   for f in glob.glob ("*."+ext):
       os.remove(f)



def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)



def HandleError(msg):
    # If msg is greater than 10 lines,
    # Replace 11th line and beyond with ellipses
    if msg.count('\n') > 10:
        msg[findnth(msg, '\n', 10):] = '...\n'
    raise VktraceException(msg)



def GetErrorMessage(out):
    matched_lines = [line for line in out.split('\n') if 'error' in line]
    return ''.join(matched_lines)



def TraceReplayProgramTest(testname, program, programArgs, args):
    print ('Beginning Trace/Replay Test: %s\n' % program)

    startTime = time.time()

    # Trace. Screenshot frame 1
    layerEnv = os.environ.copy()
    layerEnv['VK_LAYER_PATH'] = args.VkTraceLayerPath
    try:
        out = subprocess.check_output([args.VkTracePath, '-o', '%s.vktrace' % testname, '-p', program, '-a', '%s' % programArgs, '-s', '1', '-w', '.'], env=layerEnv).decode('utf-8')
    except subprocess.CalledProcessError as e:
        HandleError('Error while tracing, return code %s:\n%s' % (e.returncode, e.output))

    if 'error' in out:
        err = GetErrorMessage(out)
        HandleError('Errors while tracing:\n%s' % err)

    # Rename 1.ppm to <testname>.trace.ppm
    if os.path.exists('1.ppm'):
        os.rename('1.ppm', '%s.trace.ppm' % testname)
    else:
        HandleError('Error: Screenshot not taken while tracing.')

    # Replay
    try:
        out = subprocess.check_output([args.VkReplayPath, '-o', '%s.vktrace' % testname, '-s', '1'], env=layerEnv).decode('utf-8')
    except subprocess.CalledProcessError as e:
        HandleError('Error while replaying, return code %s:\n%s' % (e.returncode, e.output))

    if 'error' in out:
        err = GetErrorMessage(out)
        HandleError('Error while replaying:\n%s' % err)

    # Rename 1.ppm to <testname>.replay.ppm
    if os.path.exists('1.ppm'):
        os.rename('1.ppm', '%s.replay.ppm'% testname)
    else:
        HandleError ('Error: Screenshot not taken while replaying.')

    # Compare screenshots
    if not filecmp.cmp('%s.trace.ppm' % testname, '%s.replay.ppm' % testname):
        HandleError ('Error: Trace/replay screenshots do not match.')

    elapsed = time.time() - startTime

    print ('Success')
    print ('Elapsed seconds: %s\n' % elapsed)



def LoopTest(testname, program, programArgs, args):
    """ Runs a test on replay loop functionality """

    print ('Beginning Loop Test: %s\n' % program)

    startTime = time.time()

    # Trace and screenshot frame 1
    layerEnv = os.environ.copy()
    layerEnv['VK_LAYER_PATH'] = args.VkTraceLayerPath
    try:
        out = subprocess.check_output([args.VkTracePath, '-o', '%s.vktrace' % testname, '-p', program, '-a', '%s' % programArgs, '-s', '1', '-w', '.'], env=layerEnv).decode('utf-8')
    except subprocess.CalledProcessError as e:
        HandleError('Error while tracing, return code %s:\n%s' % (e.returncode, e.output))

    if 'error' in out:
        err = GetErrorMessage(out)
        HandleError('Errors while tracing:\n%s' % err)

    # Rename 1.ppm to <testname>.trace.ppm
    if os.path.exists('1.ppm'):
        os.rename('1.ppm', '%s.trace.ppm' % testname)
    else:
        HandleError('Error: Screenshot not taken while tracing.')

    # Test against 2nd loop and 3rd loop. Screenshot will always be from the last loop
    for loopCount in [2, 3]:
        # Replay
        try:
            out = subprocess.check_output([args.VkReplayPath, '-o', '%s.vktrace' % testname, '-s', '1', '-l', str(loopCount)], env=layerEnv).decode('utf-8')
        except subprocess.CalledProcessError as e:
            HandleError('Error while replaying, return code %s:\n%s' % (e.returncode, e.output))

        if 'error' in out:
            err = GetErrorMessage(out)
            HandleError('Error while replaying:\n%s' % err)

        # Rename 1.ppm to <testname>.replay.ppm
        if os.path.exists('1.ppm'):
            os.rename('1.ppm', '%s.%s.replay.ppm' % (testname, str(loopCount)))
        else:
            HandleError ('Error: Screenshot not taken while replaying.')

        # Compare screenshots
        if not filecmp.cmp('%s.trace.ppm' % testname, '%s.%s.replay.ppm' % (testname, str(loopCount))):
            HandleError ('Error: Loop Trace/replay screenshots do not match.')

    elapsed = time.time() - startTime

    print ('Success')
    print ('Elapsed seconds: %s\n' % elapsed)


if __name__ == '__main__':

    # Load settings from command-line
    parser = argparse.ArgumentParser(description='Test vktrace and vkreplay.')
    parser.add_argument('--exit-on-first-failure', action='store_true',
                        help="If set, the script will exit as soon as a failure is discovered.")
    parser.add_argument('VkTracePath', help='directory containing vktrace')
    parser.add_argument('VkTraceLayerPath', help='directory containing vktrace layer')
    parser.add_argument('VkReplayPath', help='directory containing vkreplay')
    args = parser.parse_args()
    errorMessages = []

    rmfileext("vktrace")
    rmfileext("ppm")

    try:

        # Copy the screenshot layer to the VkTraceLayerPath dir so that the loader will find it
        sspath = os.getenv('SCREENSHOT_LAYER_PATH')
        if sspath is None or sspath == '':
            if sys.platform.startswith("win"):
                sspath='..\..\../VulkanTools/build/layersvt/Debug'
            else:
                sspath='../../../VulkanTools/build/layersvt'

        if sys.platform.startswith("win"):
            shutil.copyfile(sspath + '\VkLayer_screenshot.dll', args.VkTraceLayerPath + '\VkLayer_screenshot.dll')
        else:
            shutil.copyfile(sspath + '/libVkLayer_screenshot.so', args.VkTraceLayerPath + '/libVkLayer_screenshot.so')
        shutil.copyfile(sspath + '/VkLayer_screenshot.json', args.VkTraceLayerPath + '/VkLayer_screenshot.json')

        # Get vkcube executable path from PATH
        cubePath = shutil.which('vkcube')
        if (cubePath is None):
            HandleError('Error: vkcube executable not found')

        # Trace/replay test on vkcube
        TraceReplayProgramTest('vkcube', cubePath, '--c 50', args)

        # Run loop test on cube
        LoopTest('cube-loop', cubePath, '--c 50', args)

        # Remove copies of screenshot layer files
        if sys.platform.startswith("win"):
            os.remove(args.VkTraceLayerPath + '/VkLayer_screenshot.dll')
        else:
            os.remove(args.VkTraceLayerPath + '/libVkLayer_screenshot.so')
        os.remove(args.VkTraceLayerPath + '/VkLayer_screenshot.json')

    except VktraceException as e:
        errorMessages.append(str(e))
        if args.exit_on_first_failure:
            sys.exit(1)

    if errorMessages:
        print("****************************************************")
        print("Error messages during execution:")
        print('\n'.join(errorMessages))
        sys.exit(1)

    sys.exit(0)

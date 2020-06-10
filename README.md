# vktrace

This project provides the vktrace capture/replay tool and vktrace tests. Note that vktrace has been deprecated and replaced with gfxreconstruct (git@github.com:LunarG/gfxreconstruct.git). This source is provided as a reference. If you desire to make changes to code in this repo, please fork this repo and make changes in your own copy. No contributions are being acceped for this project.

## CI Testing

Since this project is deprecated, no Continuous Intergration tests are run agains the source in this project. There do exists several tests in the test directory that you can run to test basic functionalty after you have made a source change.

## How to Build and Run

[BUILD.md](BUILD.md)
includes directions for building all the components and running the tests.

## Version Tagging Scheme

Updates to the `LunarG-vktrace` repository which correspond to a new Vulkan specification release are tagged using the following format: `v<`_`version`_`>` (e.g., `v1.1.96`).

## License
This work is released as open source under a Apache-style license from Khronos including a Khronos copyright.

See COPYRIGHT.txt for a full list of licenses used in this repository.

## Acknowledgements
While this project was developed primarily by LunarG, Inc., there are many other
companies and individuals that made this possible: Valve Corporation, funding
project development; Google providing significant contributions to the validation layers;
Khronos providing oversight and hosting of the project.

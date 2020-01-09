
if (NOT WIN32)
    # extra setup for out-of-tree builds
    if (NOT (CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_CURRENT_BINARY_DIR))
        add_custom_target(vt_test-dir-symlinks ALL
            COMMAND ln -sf ${CMAKE_CURRENT_SOURCE_DIR}/vktracereplay.sh
            COMMAND ln -sf ${CMAKE_CURRENT_SOURCE_DIR}/vktracereplay.py
            VERBATIM
            )
        set_target_properties(vt_test-dir-symlinks PROPERTIES FOLDER ${VKTRACE_TARGET_FOLDER})
    endif()
else()
    if (NOT (CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_CURRENT_BINARY_DIR))
        FILE(TO_NATIVE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/_vktracereplay.ps1 VKTRACEREPLAY)
        FILE(TO_NATIVE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/vktracereplay.py VKTRACETESTS)
        add_custom_target(vt_test-dir-symlinks ALL
            COMMAND ${CMAKE_COMMAND} -E copy_if_different ${VKTRACEREPLAY} _vktracereplay.ps1
            COMMAND ${CMAKE_COMMAND} -E copy_if_different ${VKTRACETESTS} vktracereplay.py
            VERBATIM
            )
    endif()
endif()

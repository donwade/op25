/*
 * Copyright 2022 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(analog_udp.h)                                              */
/* BINDTOOL_HEADER_FILE_HASH(3a623e992eb22a5ac9e4b4b346dbb14a)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/op25_repeater/analog_udp.h>
// pydoc.h is automatically generated in the build directory
#include <analog_udp_pydoc.h>

void bind_analog_udp(py::module& m)
{

    using analog_udp    = ::gr::op25_repeater::analog_udp;


    py::class_<analog_udp, gr::block, gr::basic_block,
        std::shared_ptr<analog_udp>>(m, "analog_udp", D(analog_udp))

        .def(py::init(&analog_udp::make),
           py::arg("options"),
           py::arg("debug"),
           py::arg("msgq_id"),
           py::arg("queue"),
           D(analog_udp,make)
        )
        




        
        .def("set_debug",&analog_udp::set_debug,       
            py::arg("debug"),
            D(analog_udp,set_debug)
        )

        ;




}









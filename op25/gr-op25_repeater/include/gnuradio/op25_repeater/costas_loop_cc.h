/* -*- c++ -*- */
/*
 * Copyright 2006,2011,2012,2014 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_OP25_REPEATER_COSTAS_LOOP_CC_H
#define INCLUDED_OP25_REPEATER_COSTAS_LOOP_CC_H

#include <gnuradio/op25_repeater/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
namespace op25_repeater {

/*!
 * \brief A Costas loop carrier recovery module.
 * \ingroup synchronizers_blk
 *
 * \details
 * The Costas loop locks to the center frequency of a signal and
 * downconverts it to baseband.
 *
 * \li When order=2: used for BPSK where the real part of the
 * output signal is the baseband BPSK signal and the imaginary
 * part is the error signal.
 *
 * \li When order=4: can be used for QPSK where both I and Q (real
 * and imaginary) are outputted.
 *
 * \li When order=8: used for 8PSK.
 *
 * More details can be found online:
 *
 * J. Feigin, "Practical Costas loop design: Designing a simple
 * and inexpensive BPSK Costas loop carrier recovery circuit," RF
 * signal processing, pp. 20-36, 2002.
 *
 * http://rfdesign.com/images/archive/0102Feigin20.pdf
 *
 * The Costas loop has one output stream:
 * \li stream 1 (required) is the baseband I and Q;
 *
 */
class OP25_REPEATER_API costas_loop_cc : virtual public sync_block
{
public:
    // gr::digital::costas_loop_cc::sptr
    typedef std::shared_ptr<costas_loop_cc> sptr;

    /*!
     * Make a Costas loop carrier recovery block.
     *
     * \param loop_bw  internal 2nd order loop bandwidth (~ 2pi/100)
     * \param order the loop order, either 2, 4, or 8
     */
    static sptr make(float loop_bw, int order, float max_phase);

    /*!
     * Returns the current value of the loop error.
     */
    virtual float error() const = 0;
    virtual float get_phase() const = 0;
    virtual void set_frequency(float freq) { }
    virtual void set_phase(float phase) { }
    virtual void set_max_phase(float phase) { }
};

} /* namespace op25_repeater */
} /* namespace gr */

#endif /* INCLUDED_OP25_REPEATER_COSTAS_LOOP_CC_H */

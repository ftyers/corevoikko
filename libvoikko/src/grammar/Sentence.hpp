/* Libvoikko: Library of Finnish language tools
 * Copyright (C) 2009 Harri Pitkänen <hatapitk@iki.fi>
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 *********************************************************************************/

#ifndef VOIKKO_GRAMMAR_SENTENCE
#define VOIKKO_GRAMMAR_SENTENCE

#include "grammar/Token.hpp"

namespace libvoikko { namespace grammar {

/**
 * Grammar checker sentence.
 */
class Sentence {
	public:
		Sentence();
		
		~Sentence();
		
		/* Maximum number of tokens in a sentence */
		static const int MAX_TOKENS_IN_SENTENCE = 500;
		
		/** Type of this sentence (start type of next sentence) */
		voikko_sentence_type type;
		
		/** Array of gc tokens */
		Token tokens[MAX_TOKENS_IN_SENTENCE];
		
		/** Number of tokens in the sentence */
		size_t tokenCount;
		
		/** Position of this sentence within paragraph */
		size_t pos;
	
	private:
		Sentence(Sentence const & other);
		Sentence & operator = (const Sentence & other);
};

} }

#endif
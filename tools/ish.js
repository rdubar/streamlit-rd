/*
ISH CLOCK version 1.2

Copyright 1996-2023, Roger Dubar.

Released under the MIT Licence.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Usage: ish();

*/

function getNumberWord(x) {
  const numberWords = [
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve'
  ];

  if (x > 0 && x <= numberWords.length)
    return numberWords[x - 1];

  return x;
}

function getBitTime(m) {
  if (m <= 7 || m > 53) return 'five minutes';
  if (m <= 12 || m > 48) return 'ten minutes';
  if (m <= 17 || m > 43) return 'quarter';
  if (m <= 23 || m > 38) return 'twenty minutes';
  if (m <= 28 || m > 33) return 'twenty-five minutes';
  return m; //default
}

function getIshTime(h, m) {
  let timeQualifier;
  h = getNumberWord(h);
  if (m <= 3 || m > 57) return h + ' o\'clock';
  if (m <= 33 && m > 28) return 'half past ' + h;
  if (m < 30) {
    timeQualifier = 'past';
  } else {
    timeQualifier = 'to';
  }
  m = getBitTime(m);

  return m + ' ' + timeQualifier + ' ' + h;
}

function getDaytimeQualifier(h) {
  if (!h || h > 21) return ' at night';
  if (h < 12) return ' in the morning';
  if (h <= 17) return ' in the afternoon';
  return ' in the evening'; // default
}

function ish(h, m, s) {
  if (!h || !m) { // if no time supplied, use the system time
    const time = new Date();
    h = time.getHours();
    m = time.getMinutes();
    s = time.getSeconds();
  }

  if (!s) s = 0;
  const daytimeQualifier = getDaytimeQualifier(h);
  h = h % 12; // fix to 12 hour clock
  if (m > 57 && s > 30) m++; // round seconds
  if (m > 60) m = 0; // round up minutes
  if (m > 33) h++; // round up hours
  if (h > 12) h = 1; // the clock turns round...
  if (h === 0) h = 12;

  return 'It is about ' + getIshTime(h, m) + daytimeQualifier + '.';
}

document.writeln(ish());

/// \file Header file

/// \name Test entry
/// \desc A whole lot of stuff

// These comments are not shown

///
/// \func A function name
/// \parm Some parameters
/// \retu Return Values
/// \desc A whole lot of stuff
///

//{

/// <b>Longer description</b>
///  Empty lines as separator
///  HTML tags OK
///  Everything output verbatim
///
//}

CODE GOES HERE

//{ Block Opening header

///    Anything between these is put verbatim
//     But not regular comments
/// With the comment sign cut off

//} Block Closing header

///
/// \func A function name multiline \
/// continuation \
/// with more than one line \

/// \parm Some parameters
/// \retu Return Values
/// \desc A whole lot of stuff
///

//!
//! use empty comment lines to separate them
//!

//{ Block Opening header (not output)

///    Second block line 1
///    Second block
///    Second block
///    Second block line 4

#define 1234 4567   /// Single line comment, inline

//[   puts everything indiscrimately to outfile

Struct aa
{
 int www
 int rrrr;
}

//]  till here

///
#define 3333 4444   //< Single line comment, in include whole line
int value = 0;      //> Single line comment, in include whole line

//} Block Closing header

///

//{ Block Opening header (without end block )

/// till the EOF
/// till the EOF
/// will show until the EOF

int value2 = 0;      //> Single line comment, in include whole line



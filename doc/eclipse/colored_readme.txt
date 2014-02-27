Simple way to have syntax highlighting in eclipse with cog templates
Get the colored plugin from http://colorer.sourceforge.net/eclipsecolorer/

Add cog to the regular expression describing python filenames in the file
eclipse/plugins/net.sf.colorer_X.X.X/colorer/hrc/proto.hrc.

The line
<filename>/\.(py|pyw|pys)$/i</filename>
Should be
<filename>/\.(py|pyw|pys|cog)$/i</filename>

# ApiCov

This is Github App that is responsible for parsing all the coverage files and uploading them to the server.
The action should also identify the APIs of interest based on the libraries being built. 
As the GitHub workflow starts there will be two stages of interest to this action.
* The build process which generates shared libraries. We would need the shared libraries to get the list of symbols from there as a superset of the APIs. 
* Depending on the build system we run `make install -n` or `ninja install -n` or `meson install --dry-run` to get the list of headers that would be installed.
* We then check our superset against that list and find out our exports.
* This step produces the list of APIs this library provides for clients to use. 
* We then move to the running gcov on all the gcno files.
* Collect all API cov data.
* upload the data for visualisation.

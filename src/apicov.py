import argparse
import logging
import json
import sys
from modules.ExportFetcher import ExportFetcher
from modules.Utils import identify_build_system, find_shared_libraries
from modules.Coverage import LibCoverage

def main():
    parser = argparse.ArgumentParser(description="Code SA API Coverage Tool")
    parser.add_argument('project_dir', type=str, help='Path to the root directory')
    parser.add_argument('install_dir', type=str, help='Path to where the built library is installed')
    parser.add_argument('--log', type=str, default='info', help='Logging level (debug, info, warning, error, critical)')

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log.upper(), None))

    shared_libs = find_shared_libraries(args.project_dir)

    lib_exports = ExportFetcher(args.project_dir)
    for lib in shared_libs:
        lib_exports.get_exports_from_lib(lib)

    build_system = identify_build_system(args.project_dir)
    if build_system == 'unknown':
        logging.error("Unsupported or unknown build system")
        return

    # lib_exports.run_install_command(build_system)

    # lib_exports.get_install_headers(build_system)
    lib_exports.filter_non_apis(args.install_dir)

    json_data = {"library": lib_exports.apis, "headers": lib_exports.headers}
    with open('apis.json', 'w') as fh:
        json.dump(json_data, fh)
    
    entry_cov = LibCoverage(lib_exports.apis, args.project_dir)
    entry_cov.run_gcov_on_gcno_files()
    entry_cov.populate_entry_api_cov()

    json_data = {}
    failed_apis = []
    for api in lib_exports.apis:
        if api in entry_cov.api_sizes:
            json_data[api] = {}
            json_data[api]["Size"] = entry_cov.api_sizes[api]
            json_data[api]["Cov"] = entry_cov.api_coverage[api]
        else:
            logging.error("Failed to find size for API: %s", api)
            failed_apis.append(api)
    with open('api_coverage.json', 'w') as fh:
        json.dump(json_data, fh)



if __name__ == "__main__":
    main()
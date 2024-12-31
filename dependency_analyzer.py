import os
import ast
import sys
from typing import Set, Dict, List
from pathlib import Path
from datetime import datetime
import io

class ImportAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.imports = set()
        self.from_imports = {}
        
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
            
    def visit_ImportFrom(self, node):
        if node.module is not None:
            module = node.module
            if node.level > 0:
                module = '.' * node.level + module
            if module not in self.from_imports:
                self.from_imports[module] = []
            for alias in node.names:
                self.from_imports[module].append(alias.name)

def analyze_file_imports(file_path: str) -> tuple[set, dict]:
    """Analyze a single file for its imports."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read())
                analyzer = ImportAnalyzer()
                analyzer.visit(tree)
                return analyzer.imports, analyzer.from_imports
            except Exception as e:
                print(f"Error parsing {file_path}: {str(e)}")
                return set(), {}
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return set(), {}

def find_python_files(directory: str) -> Dict[str, str]:
    """Build a mapping of module names to file paths."""
    module_map = {}
    directory = os.path.abspath(directory)
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory)
                module_name = os.path.splitext(rel_path)[0].replace(os.sep, '.')
                module_map[module_name] = file_path
                
                if file == '__init__.py':
                    package_name = os.path.dirname(rel_path).replace(os.sep, '.')
                    if package_name:
                        module_map[package_name] = file_path
    
    return module_map

def resolve_relative_import(current_module: str, relative_import: str) -> str:
    """Resolve a relative import to its absolute module path."""
    dots = 0
    while relative_import.startswith('.'):
        dots += 1
        relative_import = relative_import[1:]
    
    current_parts = current_module.split('.')
    if dots > len(current_parts):
        return None
    
    if relative_import:
        return '.'.join(current_parts[:-dots] + [relative_import])
    return '.'.join(current_parts[:-dots])

def analyze_dependencies(start_file: str, root_dir: str) -> Dict[str, Set[str]]:
    """Analyze all dependencies starting from a given file."""
    module_map = find_python_files(root_dir)
    analyzed = set()
    dependencies = {}
    
    def analyze_module(module_name: str):
        if module_name in analyzed:
            return
        
        analyzed.add(module_name)
        file_path = module_map.get(module_name)
        if not file_path:
            return
        
        imports, from_imports = analyze_file_imports(file_path)
        deps = set()
        
        # Handle regular imports
        for imp in imports:
            if imp in module_map:
                deps.add(imp)
        
        # Handle from imports
        for module, _ in from_imports.items():
            if module.startswith('.'):
                abs_module = resolve_relative_import(module_name, module)
                if abs_module and abs_module in module_map:
                    deps.add(abs_module)
            elif module in module_map:
                deps.add(module)
        
        dependencies[module_name] = deps
        for dep in deps:
            analyze_module(dep)
    
    # Convert start_file to module name
    rel_path = os.path.relpath(start_file, root_dir)
    start_module = os.path.splitext(rel_path)[0].replace(os.sep, '.')
    
    analyze_module(start_module)
    return dependencies

def print_tree(dependencies: Dict[str, Set[str]], root: str, seen: Set[str] = None, prefix: str = "", output_buffer: io.StringIO = None):
    """Print dependency tree in a hierarchical format."""
    if seen is None:
        seen = set()
    
    line = f"{prefix}{root}"
    print(line)
    if output_buffer:
        output_buffer.write(line + "\n")
    
    if root in seen:
        line = f"{prefix}  (circular dependency)"
        print(line)
        if output_buffer:
            output_buffer.write(line + "\n")
        return
    
    seen.add(root)
    if root in dependencies:
        for dep in sorted(dependencies[root]):
            print_tree(dependencies, dep, seen.copy(), prefix + "  ", output_buffer)

def ensure_output_dir():
    """Create the output directory if it doesn't exist."""
    output_dir = "z-dep-outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def get_unique_dependencies(dependencies: Dict[str, Set[str]], root: str, seen: Set[str] = None) -> Set[str]:
    """Get a set of all unique dependencies."""
    if seen is None:
        seen = set()
    
    if root in seen:
        return set()
    
    seen.add(root)
    unique_deps = {root}
    
    if root in dependencies:
        for dep in dependencies[root]:
            unique_deps.update(get_unique_dependencies(dependencies, dep, seen))
    
    return unique_deps

def main():
    if len(sys.argv) != 2:
        print("Usage: python dependency_analyzer.py <file_path>")
        return

    file_path = os.path.abspath(sys.argv[1])
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    root_dir = os.path.abspath(os.getcwd())
    rel_path = os.path.relpath(file_path, root_dir)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Create output directory and prepare output files
    output_dir = ensure_output_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tree_filename = f"{base_name}_{timestamp}_tree.txt"
    unique_filename = f"{base_name}_{timestamp}_unique.txt"
    tree_path = os.path.join(output_dir, tree_filename)
    unique_path = os.path.join(output_dir, unique_filename)
    
    # Create string buffers for output
    tree_buffer = io.StringIO()
    unique_buffer = io.StringIO()
    
    # Write header information
    header = f"\nDependency Analysis\n{'='*50}\n"
    header += f"File: {rel_path}\n"
    header += f"Project root: {root_dir}\n"
    header += f"Analysis date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    header += f"{'='*50}\n\n"
    
    print(header)
    tree_buffer.write(header)
    unique_buffer.write(header)
    
    try:
        dependencies = analyze_dependencies(file_path, root_dir)
        if dependencies:
            # Generate and save tree view
            title = "Dependency Tree:"
            print(title)
            tree_buffer.write(title + "\n")
            
            start_module = os.path.splitext(os.path.relpath(file_path, root_dir))[0].replace(os.sep, '.')
            print_tree(dependencies, start_module, output_buffer=tree_buffer)
            
            with open(tree_path, 'w', encoding='utf-8') as f:
                f.write(tree_buffer.getvalue())
            
            # Generate and save unique dependencies
            unique_deps = get_unique_dependencies(dependencies, start_module)
            unique_title = "\nUnique Dependencies:"
            print(unique_title)
            unique_buffer.write(unique_title + "\n")
            
            # Sort and write unique dependencies
            for dep in sorted(unique_deps):
                line = f"- {dep}"
                print(line)
                unique_buffer.write(line + "\n")
            
            with open(unique_path, 'w', encoding='utf-8') as f:
                f.write(unique_buffer.getvalue())
            
            print(f"\nOutputs saved to:")
            print(f"Tree view: {tree_path}")
            print(f"Unique dependencies: {unique_path}")
            
    except Exception as e:
        error_msg = f"Error analyzing dependencies: {str(e)}"
        print(error_msg)
        tree_buffer.write("\n" + error_msg)
        unique_buffer.write("\n" + error_msg)
    finally:
        tree_buffer.close()
        unique_buffer.close()

if __name__ == "__main__":
    main() 
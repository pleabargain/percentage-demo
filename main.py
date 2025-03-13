import random
import svgwrite
import os
import math
import logging
from datetime import datetime
import re
from colorama import init, Fore, Back, Style
import platform

# Initialize colorama for cross-platform colored text
init()

# Set up logging
logging.basicConfig(
    filename='error.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

logger = logging.getLogger(__name__)

def clear_screen():
    """Clear the terminal screen based on OS"""
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('clear')

def print_welcome():
    """Display welcome message and instructions"""
    clear_screen()
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║        Percentage Relationship Visualizer v1.0           ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}About:{Style.RESET_ALL}")
    print("This tool demonstrates the mathematical principle that")
    print(f"{Fore.GREEN}a% of b = b% of a{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}For example:{Style.RESET_ALL}")
    print("25% of 40 = 40% of 25 = 10")
    print("This works because: (a × b) ÷ 100 = (b × a) ÷ 100")
    
    print(f"\n{Fore.YELLOW}Instructions:{Style.RESET_ALL}")
    print("1. Enter calculations in the format: '25% of 40'")
    print("2. Use integers or decimals (e.g., '3.5% of 200')")
    print("3. Press Enter for a random problem")
    print(f"4. Type '{Fore.RED}EXIT{Style.RESET_ALL}' to quit")
    
    print(f"\n{Fore.YELLOW}Outputs:{Style.RESET_ALL}")
    print("- SVG and PNG visualizations will be generated")
    print("- Files are named based on the calculation")
    print(f"- Check {Fore.GREEN}error.log{Style.RESET_ALL} for any issues\n")
    
    input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    clear_screen()

def explain_principle(a, b, result):
    """Explain the percentage exchangeability principle with the current example"""
    print(f"\n{Fore.YELLOW}Understanding the Principle:{Style.RESET_ALL}")
    print(f"When we calculate {Fore.GREEN}{a}% of {b}{Style.RESET_ALL}, we're finding:")
    print(f"  ({a} × {b}) ÷ 100 = {result:.2f}")
    print(f"\nThis is mathematically identical to {Fore.GREEN}{b}% of {a}{Style.RESET_ALL}:")
    print(f"  ({b} × {a}) ÷ 100 = {result:.2f}")
    print("\nThis works because multiplication is commutative (order doesn't matter)")
    print(f"and division by 100 is constant for both calculations.{Style.RESET_ALL}")

def check_dependencies():
    """Check if all required dependencies are installed"""
    missing_deps = []
    try:
        import svgwrite
    except ImportError:
        missing_deps.append("svgwrite")
        logger.error("Missing dependency: svgwrite")
    
    try:
        import cairosvg
    except ImportError:
        missing_deps.append("cairosvg")
        logger.error("Missing dependency: cairosvg")
    
    return missing_deps

def generate_filename(a, b):
    """Generate filename based on the problem"""
    try:
        filename = f"{a}percent_of_{b}"
        logger.debug(f"Generated filename: {filename}")
        return filename
    except Exception as e:
        logger.error(f"Error generating filename: {str(e)}")
        raise

def parse_input(user_input):
    """Parse user input in format 'X% of Y' where X and Y can be integers or floats"""
    try:
        # Remove extra spaces and convert to lowercase
        cleaned_input = user_input.strip().lower()
        
        # Regular expression to match "X% of Y" format
        pattern = r'^([\d.]+)%\s*of\s*([\d.]+)$'
        match = re.match(pattern, cleaned_input)
        
        if not match:
            logger.error(f"Invalid input format: {user_input}")
            return None, None
        
        try:
            a = float(match.group(1))  # percentage
            b = float(match.group(2))  # number
            
            # Validate ranges
            if a < 0 or b < 0:
                logger.error(f"Negative numbers not allowed: {user_input}")
                return None, None
            
            logger.info(f"Successfully parsed input: {a}% of {b}")
            return a, b
        except ValueError as e:
            logger.error(f"Error converting numbers: {str(e)}")
            return None, None
            
    except Exception as e:
        logger.error(f"Error parsing input: {str(e)}")
        return None, None

def get_user_input():
    """Prompt user for input and validate"""
    while True:
        print(f"\n{Fore.CYAN}Enter a percentage calculation {Style.RESET_ALL}(e.g., '25% of 3' or '3.5% of 200')")
        print(f"Or press {Fore.GREEN}Enter{Style.RESET_ALL} for a random problem")
        print(f"Type {Fore.RED}EXIT{Style.RESET_ALL} to quit")
        
        user_input = input(f"{Fore.YELLOW}> {Style.RESET_ALL}").strip()
        
        if user_input.upper() == 'EXIT':
            return None, None
        
        # If empty, generate random problem
        if not user_input:
            a = round(random.uniform(0.1, 100.0), 2)
            b = round(random.uniform(0.1, 100.0), 2)
            logger.info(f"Generated random problem: {a}% of {b}")
            return a, b
        
        # Parse user input
        a, b = parse_input(user_input)
        if a is not None and b is not None:
            return a, b
        
        print(f"{Fore.RED}Invalid input format. Please use format: 'X% of Y' where X and Y are positive numbers.{Style.RESET_ALL}")

def generate_percentage_problem(a=None, b=None):
    """Generate or calculate percentage problem"""
    try:
        if a is None or b is None:
            a = round(random.uniform(0.1, 100.0), 2)
            b = round(random.uniform(0.1, 100.0), 2)
        
        result = (a * b) / 100
        logging.info(f"Calculated problem: {a}% of {b} = {result}")
        return a, b, result
    except Exception as e:
        logging.error(f"Error in generate_percentage_problem: {str(e)}")
        raise

def svg_to_png(svg_path, png_path):
    """Convert SVG to PNG using cairosvg"""
    try:
        import cairosvg
        
        if not os.path.exists(svg_path):
            logger.error(f"SVG file not found: {svg_path}")
            return False

        # Ensure the directory exists
        png_dir = os.path.dirname(png_path)
        if png_dir and not os.path.exists(png_dir):
            os.makedirs(png_dir)
            logger.info(f"Created directory: {png_dir}")

        # Convert SVG to PNG
        cairosvg.svg2png(url=svg_path, write_to=png_path)
        logger.info(f"Successfully generated PNG file: {png_path}")
        return True
    except ImportError:
        logger.error("cairosvg not installed. Please install with: pip install cairosvg")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in PNG conversion: {str(e)}")
        return False

def render_math_as_svg(a, b, result):
    """Render the mathematical problem as an SVG image"""
    try:
        # Generate filename based on the problem
        base_filename = generate_filename(a, b)
        svg_filename = f"{base_filename}.svg"
        png_filename = f"{base_filename}.png"
        
        # Ensure the directory exists
        output_dir = os.path.dirname(svg_filename)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created directory: {output_dir}")

        # Create SVG document
        try:
            dwg = svgwrite.Drawing(svg_filename, (500, 300), profile='tiny')
        except Exception as e:
            logger.error(f"Failed to create SVG drawing: {str(e)}")
            raise

        # Add white background
        dwg.add(dwg.rect((0, 0), (500, 300), fill='white'))
        
        # Define styles using proper SVG attributes
        title_attrs = {
            "font-family": "Arial",
            "font-size": "24px",
            "font-weight": "bold",
            "text-anchor": "middle"
        }
        math_attrs = {
            "font-family": "Times New Roman",
            "font-size": "28px",
            "text-anchor": "middle"
        }
        result_attrs = {
            "font-family": "Times New Roman",
            "font-size": "28px",
            "fill": "#0066CC",
            "text-anchor": "middle"
        }
        
        # Add title
        dwg.add(dwg.text(
            "Percentage Relationship Demonstration",
            insert=(250, 50),
            **title_attrs
        ))
        
        # Format problem
        problem1 = f"{a}% of {b} = {result:.2f}"
        problem2 = f"{b}% of {a} = {result:.2f}"
        formula = f"(a × b) ÷ 100 = ({a} × {b}) ÷ 100 = {result:.2f}"
        
        # Add explanation
        y_pos = 100
        dwg.add(dwg.text(problem1, insert=(250, y_pos), **math_attrs))
        
        y_pos += 50
        dwg.add(dwg.text(problem2, insert=(250, y_pos), **math_attrs))
        
        # Add dividing line
        y_pos += 40
        dwg.add(dwg.line((50, y_pos), (450, y_pos), stroke="#333333", stroke_width=2))
        
        # Add formula
        y_pos += 50
        dwg.add(dwg.text("General formula:", insert=(250, y_pos), **math_attrs))
        
        y_pos += 50
        dwg.add(dwg.text(formula, insert=(250, y_pos), **result_attrs))
        
        # Save the SVG
        try:
            dwg.save()
            logger.info(f"Successfully generated SVG file: {svg_filename}")
        except PermissionError as e:
            logger.error(f"Permission denied while saving SVG: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to save SVG file: {str(e)}")
            raise

        # Convert to PNG using cairosvg
        png_success = svg_to_png(svg_filename, png_filename)
        if not png_success:
            logger.warning(f"PNG conversion failed for {svg_filename}")
        
        return svg_filename, png_filename if png_success else None
            
    except Exception as e:
        logger.error(f"Error in render_math_as_svg: {str(e)}")
        raise

def generate_multiple_problems(num_problems=5):
    """Generate multiple random percentage problems and render them as SVGs"""
    try:
        for i in range(num_problems):
            a, b, result = generate_percentage_problem()
            svg_file, png_file = render_math_as_svg(a, b, result)
            print(f"Problem {i+1}: {a}% of {b} = {b}% of {a} = {result:.2f}")
        logging.info(f"Successfully generated {num_problems} problems")
    except Exception as e:
        logging.error(f"Error in generate_multiple_problems: {str(e)}")
        raise

def main():
    try:
        # Display welcome message
        print_welcome()
        
        # Check dependencies first
        missing_deps = check_dependencies()
        if missing_deps:
            deps_str = ", ".join(missing_deps)
            logger.error(f"Missing required dependencies: {deps_str}")
            print(f"{Fore.RED}Please install missing dependencies: {deps_str}{Style.RESET_ALL}")
            return

        while True:
            # Get user input
            a, b = get_user_input()
            
            # Check for exit condition
            if a is None and b is None:
                print(f"\n{Fore.CYAN}Thank you for using the Percentage Relationship Visualizer!{Style.RESET_ALL}")
                break
            
            # Generate and display the problem
            a, b, result = generate_percentage_problem(a, b)
            svg_file, png_file = render_math_as_svg(a, b, result)
            
            print(f"\n{Fore.GREEN}Files generated:{Style.RESET_ALL}")
            print(f"SVG: {svg_file}")
            if png_file:
                print(f"PNG: {png_file}")
            else:
                print(f"{Fore.RED}PNG conversion not available. Check error.log for details.{Style.RESET_ALL}")
            
            # Display and explain the relationship
            print(f"\n{Fore.CYAN}Mathematical relationship:{Style.RESET_ALL}")
            print(f"{a}% of {b} = {result:.2f}")
            print(f"{b}% of {a} = {result:.2f}")
            
            explain_principle(a, b, result)
            
            print(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            input()
            clear_screen()
            
    except Exception as e:
        logger.error(f"Unexpected error in main: {str(e)}")
        print(f"{Fore.RED}An error occurred. Check error.log for details.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
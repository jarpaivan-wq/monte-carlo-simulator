# Monte Carlo Simulator - Base Module

A flexible and powerful tool for performing Monte Carlo simulations with an intuitive graphical interface. Perfect for statistical analysis, risk modeling, and predictions.

## ✨ Features

- **Multiple Probability Distributions**
  - Normal (Gaussian)
  - Uniform
  - Triangular
  - Log-normal
  - Binomial
  - Poisson

- **Intuitive Graphical Interface**
  - Visual configuration of variables
  - Formula editor
  - Real-time graphics
  - Complete statistics

- **Analysis Tools**
  - Goal Evaluator: Calculates the probability of reaching a target value
  - Result Estimator: Predicts the result for specific values
  - Percentile analysis
  - 95% confidence interval

- **Complete Statistics**
  - Mean, median, standard deviation
  - Minimum and maximum
  - Percentiles (2.5, 25, 75, 97.5)
  - Distribution histograms

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/your-username/monte-carlo-simulator.git
cd monte-carlo-simulator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python monte_carlo_simulator.py
```

## 📖 Usage

### Basic Example: Monthly Income Simulation

Suppose you want to simulate monthly income based on:
- Unit price (normal distribution: mean 100, standard deviation 10)
- Quantity sold (uniform distribution: 50-150 units)

**Steps:**

1. **Add Variables**
   - Name: `price`
   - Distribution: Normal
   - Mean: 100
   - Standard Deviation: 10
   - Click "Add Variable"

2. **Add second variable**
   - Name: `quantity`
   - Distribution: Uniform
   - Minimum: 50
   - Maximum: 150
   - Click "Add Variable"

3. **Enter the Formula**
   - In the "Formula" field, type: `price * quantity`

4. **Run Simulation**
   - Number of simulations: 10000
   - Click "RUN SIMULATION"

5. **Analyze Results**
   - View the histogram with income distribution
   - Review statistics (mean, percentiles, etc.)
   - Use the "Goal Evaluator" to determine the probability of reaching 15000 in income
   - Use the "Result Estimator" to see what happens with a price of 120

### Advanced Example: Financial Risk Analysis

Simulate investment return considering:
- Asset A return (normal: mean 8%, std 2%)
- Asset B return (normal: mean 12%, std 4%)
- Portfolio weight A (uniform: 30-70%)

**Formula:** `(A * weight_a) + (B * (100 - weight_a)) / 100`

### Available Distributions

#### Normal (Gaussian)
```
Parameters: mean, standard_deviation
Use: For variables distributed symmetrically
Example: Height of people, measurement errors
```

#### Uniform
```
Parameters: minimum, maximum
Use: When all values in a range have equal probability
Example: Number of customers per day, waiting time
```

#### Triangular
```
Parameters: minimum, mode, maximum
Use: When you have a most likely value between two extremes
Example: Project cost estimates
```

#### Log-normal
```
Parameters: mean_log, standard_deviation_log
Use: For positive variables with right skew
Example: Salaries, equipment lifespan
```

#### Binomial
```
Parameters: n (number of trials), p (probability of success)
Use: To count successes in n independent attempts
Example: Number of closed sales out of 100 attempts
```

#### Poisson
```
Parameters: lambda (occurrence rate)
Use: To count events in a time period
Example: Number of calls per hour, defects per batch
```

## 🧮 Supported Formulas

The tool supports:

**Basic Operations:**
- Addition: `a + b`
- Subtraction: `a - b`
- Multiplication: `a * b`
- Division: `a / b`
- Power: `a ** b` or `pow(a, b)`

**Mathematical Functions:**
- Square root: `sqrt(a)`
- Exponential: `exp(a)`
- Natural logarithm: `log(a)`
- Sine: `sin(a)` (in radians)
- Cosine: `cos(a)`
- Tangent: `tan(a)`
- Absolute value: `abs(a)`

**Comparison Functions:**
- Minimum: `min(a, b)`
- Maximum: `max(a, b)`

**Complex Formula Examples:**
```
x + y * 2
sqrt(x) + log(y)
max(x, y) * min(a, b)
(x + y) / (1 + z)
exp(x) - 2 * y
```

## 📊 Results Interpretation

### Main Statistics

- **Mean**: Expected average of the results
- **Median**: Central value that divides the results in half
- **Standard Deviation**: Measures the variability of results
- **Percentile 2.5 and 97.5**: Define the 95% confidence interval

### Analysis Tools

**Goal Evaluator:**
- Enter a target value
- Shows what percentile that value is in
- Tells you the probability of reaching or exceeding that target
- Green: >50% probability (very likely)
- Orange: 25-50% probability (possible)
- Red: <25% probability (unlikely)

**Result Estimator:**
- Enter a specific value for a variable
- Shows the expected result of the formula
- Indicates what percentile that result falls in
- Useful for "what-if" analysis

## 💡 Use Cases

### Finance
- Investment return analysis
- Credit risk assessment
- Cash flow simulation
- Option valuation

### Operations
- Project cost estimation
- Production capacity analysis
- Inventory management
- Delivery time estimates

### Research
- Statistical data analysis
- Complex systems modeling
- Hypothesis validation
- Sensitivity studies

## 🛠️ Technical Requirements

```
Python >= 3.7
numpy >= 1.19.0
matplotlib >= 3.3.0
scipy >= 1.5.0
tkinter (included with Python)
```

See `requirements.txt` for more details.

## 📝 Code Structure

The script includes the following classes:

- **Variable**: Represents a random variable with its distribution
- **Model**: Defines the relationship between variables through a formula
- **Simulator**: Main engine that executes the simulations
- **Results**: Stores and analyzes results
- **AplicacionMonteCarlo**: Main graphical interface

## 🤝 Contributions

Contributions are welcome. If you have suggestions or find bugs:

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/MyFeature`)
3. Commit your changes (`git commit -m 'Add MyFeature'`)
4. Push to the branch (`git push origin feature/MyFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## 👨‍💻 Author

Developed as a flexible statistical analysis tool.

## ❓ Frequently Asked Questions

**Q: How many simulations should I use?**
A: Generally 10,000 is a good starting point. For more accurate analysis, use 100,000 or more.

**Q: Can I use more than one variable in the formula?**
A: Yes, you can use all the variables you add. Simply use them in the formula by their name.

**Q: What happens if my formula has an error?**
A: The application will show an error message. Verify that all variables used in the formula are defined.

**Q: Can I export the results?**
A: Currently, results are displayed graphically. You can take a screenshot or modify the code to export to CSV.

## 📞 Support

If you have problems or questions, open an issue on GitHub.

---

**Last update:** 2025

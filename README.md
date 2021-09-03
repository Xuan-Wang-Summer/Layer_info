# Layer_info

A tool to analysis and record parameters for each layer and generate topological order for the layers in a whole model.
Utilizing **Timeloop** developed by **NVlab**, the generated recorded paratmeters and orders can be used to estimate the computes, cycles,etc. for models.

## Usage
The scripts and templates should be directly put under the **timeloop** folder for convienent usage.
Modify **template.txt** to try more templates.
Modify parts of the **order_map.py** and **layer_problem.py** to try more models.

## Examples
Modify the following code to test on more models.
```` 
# Change the following line to use different models
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # PyTorch v0.4.0
# Change models
model = torchvision.models.resnet18().to(device)
# Change inputs
example = torch.rand(1, 3, 224, 224)
example = example.to(device)
````

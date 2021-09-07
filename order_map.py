# -*- coding: utf-8 -*-
"""order_map.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VgLrf5E0JCVSyjgJvRBc9FXo6yfFFFa7
"""

import torch
import torchvision
import operator
from collections import defaultdict
from typing import Dict
import os
import shutil 
from collections import defaultdict

# Check whether we want to include current layer
def check_valid(node) -> bool:
  result = True
  node_kind = node.kind()
  if node_kind == "onnx::Add":
    result = False
  if node_kind == "onnx::Flatten":
    result = False
  return result 

# Match the number with number of filename
def match_name(model, input):
  trace, out = torch.jit._get_trace_graph(model, input)
  torch_graph = torch.onnx._optimize_trace(trace, torch.onnx.OperatorExportTypes.ONNX)
  total_layer = 0
  for torch_node in torch_graph.nodes():
    total_layer = total_layer + 1
  result = {x: "None" for x in range(1, total_layer)}
  #Check whether the layer is valid
  total_valid = 0
  i = 0
  for torch_node in torch_graph.nodes():
    i = i + 1
    if check_valid(torch_node):
      total_valid = total_valid + 1
      result[i] = str(total_valid)
  return result

# Store the relationship of each layer
def rela(model, input, inputs, outputs, visited, pre, post):
  num_s = 1
  trace, out = torch.jit._get_trace_graph(model, input)
  torch_graph = torch.onnx._optimize_trace(trace, torch.onnx.OperatorExportTypes.ONNX)
  # Check each node and find its outputs
  for torch_node in torch_graph.nodes():
    # Check the output node
    visited[num_s] = False
    pre[num_s] = -1
    post[num_s] = -1
    start_outputs = [o.unique() for o in torch_node.outputs()]
    num_t = 1
    # Check each node and find the output node's input nodes
    for target_torch_node in torch_graph.nodes():
      target_inputs = [i.unique() for i in target_torch_node.inputs()]
      # Check whether the inputs and outputs match
      if set(start_outputs) & set(target_inputs):
        # Record the inputs for target node
        inputs[num_t].append(num_s)
        # Record the outputs for torch_node
        outputs[num_s].append(num_t)
      num_t = num_t + 1
    num_s = num_s + 1

# Find the topological order
def topo(model, input):
  # Establish inputs and outputs information for each node
  trace, out = torch.jit._get_trace_graph(model, input)
  torch_graph = torch.onnx._optimize_trace(trace, torch.onnx.OperatorExportTypes.ONNX)
  total_layer = 0
  for torch_node in torch_graph.nodes():
    total_layer = total_layer + 1
  total_layer = total_layer + 1
  inputs = {x: [] for x in range(1, total_layer)}
  outputs = {x: [] for x in range(1, total_layer)}
  visited = {"node": False}
  pre = {"node": -1}
  post = {"node": -1}
  rela(model, input, inputs, outputs, visited, pre, post)

  # Explore in DFS
  stack = []
  def explore(node: int):
    visited[node] = True
    for next in outputs[node]:
      if not visited[next]:
        explore(next)
    stack.append(node)

  # Get topological order
  explore(1)
  return stack[::-1]

# Write the order of processing files into a file line by line
def write_order(topo, match):
  filename_h = "topo_order.txt"
  filename_v = "v_order.txt"
  f_h = open(filename_h, "w+")
  f_v = open(filename_v, "w+")
  for x in topo:
    if(x != "node"):
      if(match[x] != "None"):
        f_h.write(match[x] + " ")
        f_v.write(match[x] + "\n")
  f_h.close()
  f_v.close()

# Change the following line to use different models
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # PyTorch v0.4.0
# Change models
model = torchvision.models.resnet18().to(device)
# Change inputs
example = torch.rand(1, 3, 224, 224)
example = example.to(device)
# Run the anaylsis
topo_result = topo(model, example)
match_result = match_name(model, example)
write_order(topo_result, match_result)

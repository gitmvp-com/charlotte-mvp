#!/usr/bin/env python3
"""
CHARLOTTE MVP - Code Reasoner

Simplified AI-powered code analysis using masked language models.
Supports code completion, token prediction, and option scoring.
"""

import sys
import argparse
from typing import List, Tuple

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForMaskedLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("[!] Warning: transformers not installed. Code Reasoner will not work.")
    print("    Install with: pip install transformers torch")

class CodeReasonerCLI:
    """Simple code reasoner using HuggingFace transformers"""
    
    COMMON_MASKS = ["[MASK]", "[mask]", "<MASK>", "<mask>"]
    
    def __init__(self, model_name: str = "microsoft/codebert-base", device: str = None):
        if not TRANSFORMERS_AVAILABLE:
            raise RuntimeError("transformers library not available")
        
        # Auto-detect device
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.device = torch.device(device)
        print(f"[*] Loading model: {model_name} on {device}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        self.model = AutoModelForMaskedLM.from_pretrained(model_name).to(self.device).eval()
        self.mask_token = self.tokenizer.mask_token or "<mask>"
        self.mask_token_id = int(self.tokenizer.mask_token_id)
        
        print("[✓] Model loaded successfully")
    
    def _normalize_masks(self, text: str) -> str:
        """Replace common mask variants with standard mask token"""
        result = text
        for mask in self.COMMON_MASKS:
            result = result.replace(mask, self.mask_token)
        return result
    
    @torch.inference_mode()
    def guess(self, text: str, top_k: int = 5) -> List[Tuple[int, List[Tuple[str, float]]]]:
        """Predict tokens for masked positions"""
        text = self._normalize_masks(text)
        
        if self.mask_token not in text:
            raise ValueError(f"No mask token found. Use '{self.mask_token}' in your code.")
        
        # Tokenize
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        input_ids = inputs["input_ids"]
        
        # Find mask positions
        mask_positions = (input_ids == self.mask_token_id).nonzero(as_tuple=False)
        
        if mask_positions.numel() == 0:
            raise ValueError("No mask token found after tokenization")
        
        # Get predictions
        outputs = self.model(**inputs)
        logits = outputs.logits[0]  # [seq_len, vocab_size]
        
        results = []
        for _, pos in mask_positions:
            pos = int(pos.item())
            
            # Get probabilities for this position
            token_logits = logits[pos]
            probs = torch.softmax(token_logits, dim=-1)
            
            # Get top-k predictions
            top_probs, top_indices = torch.topk(probs, k=min(top_k, probs.shape[-1]))
            
            predictions = []
            for prob, idx in zip(top_probs.tolist(), top_indices.tolist()):
                token = self.tokenizer.decode([idx]).strip()
                predictions.append((token, prob))
            
            results.append((pos, predictions))
        
        return results
    
    @torch.inference_mode()
    def fill(self, text: str, top_k: int = 3) -> List[str]:
        """Fill all masks in text with predictions"""
        text = self._normalize_masks(text)
        
        if self.mask_token not in text:
            raise ValueError(f"No mask token found. Use '{self.mask_token}' in your code.")
        
        # Get predictions for first mask
        predictions = self.guess(text, top_k=top_k)
        
        if not predictions:
            return [text]
        
        # Branch on first mask predictions
        _, first_preds = predictions[0]
        branches = []
        
        for token, _ in first_preds[:top_k]:
            # Replace first mask with predicted token
            filled = text.replace(self.mask_token, token, 1)
            
            # Recursively fill remaining masks (greedy)
            while self.mask_token in filled:
                next_preds = self.guess(filled, top_k=1)
                if not next_preds:
                    break
                _, next_tokens = next_preds[0]
                if not next_tokens:
                    break
                next_token, _ = next_tokens[0]
                filled = filled.replace(self.mask_token, next_token, 1)
            
            branches.append(filled)
        
        return branches
    
    @torch.inference_mode()
    def score(self, text: str, options: List[str]) -> List[Tuple[str, float]]:
        """Score given options for the first mask position"""
        text = self._normalize_masks(text)
        
        if self.mask_token not in text:
            raise ValueError(f"No mask token found. Use '{self.mask_token}' in your code.")
        
        # Tokenize
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        input_ids = inputs["input_ids"]
        
        # Find first mask position
        mask_positions = (input_ids == self.mask_token_id).nonzero(as_tuple=False)
        
        if mask_positions.numel() == 0:
            raise ValueError("No mask token found after tokenization")
        
        pos = int(mask_positions[0, 1].item())
        
        # Get predictions
        outputs = self.model(**inputs)
        logits = outputs.logits[0, pos]
        probs = torch.softmax(logits, dim=-1)
        
        # Score each option
        scored = []
        for option in options:
            # Tokenize option (take first token if multi-token)
            option_ids = self.tokenizer.encode(option, add_special_tokens=False)
            if not option_ids:
                continue
            
            token_id = option_ids[0]
            score = float(probs[token_id].item())
            scored.append((option, score))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored
    
    def print_guess_results(self, results: List[Tuple[int, List[Tuple[str, float]]]]):
        """Pretty print guess results"""
        for i, (pos, predictions) in enumerate(results):
            print(f"\n[Mask {i} at position {pos}]")
            for token, prob in predictions:
                print(f"  {prob*100:5.2f}%  {token!r}")
    
    def print_fill_results(self, results: List[str]):
        """Pretty print fill results"""
        print("\n[Completions]")
        for i, completion in enumerate(results, 1):
            print(f"  {i}. {completion}")
    
    def print_score_results(self, results: List[Tuple[str, float]]):
        """Pretty print score results"""
        print("\n[Scores]")
        for option, score in results:
            print(f"  {score*100:5.2f}%  {option!r}")

def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="CHARLOTTE Code Reasoner - AI-powered code analysis"
    )
    parser.add_argument(
        "--model",
        default="microsoft/codebert-base",
        help="HuggingFace model to use"
    )
    parser.add_argument(
        "--device",
        choices=["cpu", "cuda", "auto"],
        default="auto",
        help="Device to use for inference"
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Guess command
    guess_parser = subparsers.add_parser("guess", help="Predict masked tokens")
    guess_parser.add_argument("code", help="Code with [MASK] tokens")
    guess_parser.add_argument("--top-k", type=int, default=5, help="Number of predictions")
    
    # Fill command
    fill_parser = subparsers.add_parser("fill", help="Fill all masked tokens")
    fill_parser.add_argument("code", help="Code with [MASK] tokens")
    fill_parser.add_argument("--top-k", type=int, default=3, help="Number of branches")
    
    # Score command
    score_parser = subparsers.add_parser("score", help="Score options for mask")
    score_parser.add_argument("code", help="Code with [MASK] token")
    score_parser.add_argument("--options", nargs="+", required=True, help="Options to score")
    
    args = parser.parse_args()
    
    if not TRANSFORMERS_AVAILABLE:
        print("[!] Error: transformers library not installed")
        print("    Install with: pip install transformers torch")
        return 1
    
    try:
        device = None if args.device == "auto" else args.device
        reasoner = CodeReasonerCLI(model_name=args.model, device=device)
        
        if args.command == "guess":
            results = reasoner.guess(args.code, top_k=args.top_k)
            reasoner.print_guess_results(results)
        
        elif args.command == "fill":
            results = reasoner.fill(args.code, top_k=args.top_k)
            reasoner.print_fill_results(results)
        
        elif args.command == "score":
            results = reasoner.score(args.code, args.options)
            reasoner.print_score_results(results)
        
        return 0
    
    except Exception as e:
        print(f"\n[!] Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

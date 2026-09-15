import easyocr
import cv2
import numpy as np
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self, model="easy"):
        """Initialize OCR service"""
        self.model_type = model
        if model == "easy":
            self.reader = easyocr.Reader(['ro', 'en'], gpu=False)
        else:
            # Tesseract fallback
            try:
                import pytesseract
                self.reader = pytesseract
            except ImportError:
                logger.warning("Tesseract not installed, using EasyOCR")
                self.reader = easyocr.Reader(['ro', 'en'], gpu=False)

    def extract_text_from_image(self, image_data):
        """Extract text from image (base64 or file path)"""
        try:
            start_time = time.time()
            
            # Convert base64 to numpy array if needed
            if isinstance(image_data, str):
                import base64
                image_bytes = base64.b64decode(image_data)
                nparr = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            else:
                image = image_data
            
            # Extract text using EasyOCR
            results = self.reader.readtext(image)
            
            detected_text = "\n".join([text[1] for text in results])
            confidence = np.mean([text[2] for text in results]) if results else 0.0
            
            processing_time = time.time() - start_time
            
            return {
                "text": detected_text,
                "confidence": float(confidence),
                "processing_time": processing_time,
                "raw_results": results
            }
        
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            raise

    def extract_code_from_image(self, image_data):
        """Extract electronic component codes from image"""
        try:
            result = self.extract_text_from_image(image_data)
            detected_text = result["text"]
            
            # Clean and extract codes (simple pattern matching)
            codes = self._extract_component_codes(detected_text)
            
            return {
                "detected_codes": codes,
                "raw_text": detected_text,
                "confidence": result["confidence"],
                "processing_time": result["processing_time"]
            }
        
        except Exception as e:
            logger.error(f"Code extraction failed: {e}")
            raise

    def _extract_component_codes(self, text):
        """Extract electronic component codes from text"""
        import re
        
        # Patterns for common component codes
        patterns = [
            r'[A-Z]{1,3}\d{3,4}[A-Z]?',  # BC547, 2N2222
            r'[A-Z]{2}\d{4,6}',           # LM7805
            r'\b[0-9]{3,4}[RFW]\b',       # 10K, 100R (resistors)
            r'\b\d+[uUnNpP][Ff]\b',       # 100uF, 10nF (capacitors)
        ]
        
        codes = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            codes.extend(matches)
        
        return list(set(codes))  # Remove duplicates

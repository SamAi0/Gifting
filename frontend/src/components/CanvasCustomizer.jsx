import { useEffect, useRef, useState } from 'react';
import * as fabric from 'fabric';

// Development mode logger - only logs in development
const isDev = import.meta.env.DEV;
const devLog = (...args) => isDev && console.log('[CanvasCustomizer]', ...args);
const devError = (...args) => console.error('[CanvasCustomizer]', ...args);

// Mapping mode logger - ALWAYS logs when in mapping mode
const mappingLog = (...args) => console.log('[MAPPING MODE]', ...args);

/**
 * CanvasCustomizer - The core Fabric.js rendering engine for product personalization.
 * 
 * @param {Object} productConfig - Config from customization.json for the active product
 * @param {String} customText - The text to render
 * @param {String} textColor - The color of the text
 * @param {String} logoImage - Data URL of the uploaded logo
 * @param {Function} onImageExport - Callback when a high-res image is generated
 * @param {Function} onWarning - Callback when text exceeds fit boundaries
 */
const CanvasCustomizer = ({ productConfig, customText, textColor, logoImage, onImageExport, onWarning }) => {
  const canvasRef = useRef(null);
  const fabricCanvas = useRef(null);
  const containerRef = useRef(null);
  const [loading, setLoading] = useState(true);
  const [isMappingMode] = useState(() => {
    // Always enable mapping mode for coordinate picking
    return true;
  });
  const prevProductSlug = useRef(null);
  const customTextRef = useRef(customText);
  const textColorRef = useRef(textColor);

  // Keep refs updated
  useEffect(() => {
    customTextRef.current = customText;
    textColorRef.current = textColor;
  }, [customText, textColor]);

  // Removed useEffect for isMappingMode - using lazy initialization instead

  // Helper for curved text - defined at component level to be accessible by both useEffects
  const updateCurvedText = (group, text, zone, currentTextColor) => {
    if (!group || !fabricCanvas.current) return;
    
    group.removeAll();
    if (!text) return;
    
    const radius = zone.curveRadius || 150;
    const spacing = zone.charSpacing || 8; 
    const fontSize = zone.fontSize || 40;
    
    const chars = text.split('');
    const totalAngle = chars.length * spacing;
    const startAngle = -totalAngle / 2;
    
    const style = {
        fill: currentTextColor || zone.fill || '#000',
        opacity: zone.opacity || 1,
        globalCompositeOperation: zone.blendMode || 'source-over',
    };
    if (zone.effect === 'engrave') {
        style.fill = '#1a1a1a';
        style.opacity = 0.65;
        style.globalCompositeOperation = 'multiply';
        style.shadow = new fabric.Shadow({ color: 'rgba(255,255,255,0.4)', blur: 1, offsetX: 0.5, offsetY: 0.5 });
    }

    chars.forEach((char, i) => {
      const charAngle = startAngle + (i * spacing);
      const rad = charAngle * (Math.PI / 180);
      
      const charObj = new fabric.Text(char, {
        fontSize,
        fontFamily: zone.fontFamily || 'serif',
        originX: 'center',
        originY: 'bottom',
        left: radius * Math.sin(rad),
        top: -radius * Math.cos(rad) + radius, 
        angle: charAngle,
        ...style
      });
      group.add(charObj);
    });
    group.setCoords();
  };

  // Initialize Canvas
  useEffect(() => {
    if (!canvasRef.current || !productConfig || !productConfig.baseImage) {
      devLog('Missing canvas ref or productConfig');
      return;
    }

    // Prevent re-initialization if same product
    const productSlug = productConfig.baseImage;
    if (prevProductSlug.current === productSlug && fabricCanvas.current) {
      devLog('Skipping re-initialization for same product');
      return;
    }
    prevProductSlug.current = productSlug;

    // Cleanup previous instance if re-initializing
    if (fabricCanvas.current) {
      devLog('Disposing previous canvas instance');
      fabricCanvas.current.dispose();
      fabricCanvas.current = null;
    }

    // Initialize Canvas
    const initCanvas = async () => {
      if (!canvasRef.current) {
        devError('canvasRef.current is null');
        return;
      }

      try {
        fabricCanvas.current = new fabric.Canvas(canvasRef.current, {
          width: 500,
          height: 500,
          backgroundColor: '#f3f4f6',
          selection: true,
        });

        // Update image on drag and drop or modification
        fabricCanvas.current.on('object:modified', () => {
          fabricCanvas.current.requestRenderAll();
          const dataUrl = fabricCanvas.current.toDataURL({ format: 'png', quality: 1, multiplier: 2 });
          onImageExport?.(dataUrl);
        });

        console.log('✅ Canvas initialized:', fabricCanvas.current);
        devLog('Canvas initialized successfully');
        
        // Load base image after canvas is ready
        await loadBaseImage();
      } catch (error) {
        devError('Failed to initialize canvas:', error);
      }
    };

    // Wait for DOM to be ready
    const timer = setTimeout(initCanvas, 100);


    // Function to setup mapping mode handlers - ALWAYS enabled
    const setupMappingModeHandlers = () => {
      if (!fabricCanvas.current) {
        console.warn('⚠️ Cannot setup mapping handlers - canvas not ready');
        return;
      }
      
      mappingLog('🔧 Setting up coordinate mapping handlers...');
      mappingLog('📍 Click anywhere on the product image to get coordinates');
      
      // Add click event to capture coordinates - ALWAYS ACTIVE
      fabricCanvas.current.on('mouse:down', (e) => {
        try {
          // Get pointer position - Fabric v7 compatible
          let pointer;
          
          // Fabric v7+ uses different methods
          if (typeof fabricCanvas.current.getScenePoint === 'function') {
            pointer = fabricCanvas.current.getScenePoint(e.e);
          } else if (typeof fabricCanvas.current.getPointer === 'function') {
            pointer = fabricCanvas.current.getPointer(e.e);
          } else {
            // Fallback: calculate from event coordinates
            const canvasElement = fabricCanvas.current.getElement();
            const rect = canvasElement.getBoundingClientRect();
            pointer = {
              x: (e.e.clientX - rect.left) / (rect.width / 500),
              y: (e.e.clientY - rect.top) / (rect.height / 500)
            };
          }
          
          const jsonX = Math.round((pointer.x / 500) * 1000); // Convert to 0-1000 scale
          const jsonY = Math.round((pointer.y / 500) * 1000); // Convert to 0-1000 scale
          
          mappingLog('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
          mappingLog('🎯 CLICK COORDINATES (for customization.json):');
          mappingLog('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
          mappingLog(`X: ${jsonX} | Y: ${jsonY}`);
          mappingLog('📋 COPY THIS JSON SNIPPET:');
          mappingLog(JSON.stringify({ x: jsonX, y: jsonY }, null, 2));
          mappingLog('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        } catch (error) {
          console.error('❌ Error getting pointer:', error);
        }
      });
      
      mappingLog('✅ Coordinate mapping is now active!');
    };

    const loadBaseImage = async () => {
      if (!fabricCanvas.current) {
        devError('fabricCanvas is null in loadBaseImage');
        return;
      }

      try {
        setLoading(true);
        const img = await fabric.Image.fromURL(productConfig.baseImage, { crossOrigin: 'anonymous' });
        
        // Check if canvas was disposed during async operation
        if (!fabricCanvas.current) {
          devLog('Canvas disposed during image load, skipping');
          return;
        }
        
        const canvasWidth = 500;
        const canvasHeight = 500;
        
        const scaleW = canvasWidth / img.width;
        const scaleH = canvasHeight / img.height;
        const scale = Math.min(scaleW, scaleH) * 0.98; 
        
        img.set({
          scaleX: scale,
          scaleY: scale,
          left: canvasWidth / 2,
          top: canvasHeight / 2,
          originX: 'center',
          originY: 'center',
          selectable: false,
          evented: true, // Always enable events for coordinate mapping
          data: { isBaseImage: true }
        });

        fabricCanvas.current.add(img);
        initTextZones();
        fabricCanvas.current.requestRenderAll();
        devLog('Base image loaded successfully');
        
        // Setup click handler after canvas is fully loaded
        if (isMappingMode) {
          setupMappingModeHandlers();
        }
      } catch (err) {
        devError("Failed to load base image:", err);
      } finally {
        if (fabricCanvas.current) {
          setLoading(false);
        }
      }
    };

    const getZoneStyle = (zone) => {
      let style = {
        fill: textColorRef.current || zone.fill || '#000',
        opacity: zone.opacity || 1,
        globalCompositeOperation: zone.blendMode || 'source-over',
      };
      
      if (zone.shadow) {
        style.shadow = new fabric.Shadow(zone.shadow);
      }
      
      if (zone.effect === 'engrave') {
        style.fill = '#1a1a1a';
        style.opacity = 0.65;
        style.globalCompositeOperation = 'multiply';
        style.shadow = new fabric.Shadow({
          color: 'rgba(255,255,255,0.4)',
          blur: 1,
          offsetX: 0.5,
          offsetY: 0.5
        });
      }
      return style;
    };

    const initTextZones = () => {
      devLog('Initializing zones, total zones:', productConfig.zones.length);
      
      productConfig.zones.forEach((zone, index) => {
        devLog(`Creating zone ${index + 1} - ${zone.id}`);
        
        if (zone.type === 'text') {
          const left = (zone.x / 1000) * 500;
          const top = (zone.y / 1000) * 500;
          const style = getZoneStyle(zone);
          
          devLog(`Zone ${index + 1} position: x=${left}, y=${top}`);
          
          if (zone.isCurved) {
             const group = new fabric.Group([], {
               left, top,
               originX: zone.originX || 'center',
               originY: zone.originY || 'center',
               angle: zone.angle || 0,
               selectable: true,
               evented: true,
               hasControls: true,
               hasBorders: true,
               data: { zoneId: zone.id, isCurved: true, ...zone }
             });
             fabricCanvas.current.add(group);
             updateCurvedText(group, customTextRef.current || zone.placeholder, zone, textColorRef.current);
             devLog(`Zone ${index + 1} curved text created`);
          } else {
            const textObj = new fabric.Text(customTextRef.current || zone.placeholder, {
              left, top,
              originX: zone.originX || 'center',
              originY: zone.originY || 'center',
              angle: zone.angle || 0,
              fontFamily: zone.fontFamily || 'serif',
              fontSize: zone.fontSize || 40,
              textAlign: 'center',
              selectable: true,
              evented: true,
              hasControls: true,
              hasBorders: true,
              fill: textColorRef.current || zone.fill || '#000',
              ...style,
              data: { zoneId: zone.id, ...zone }
            });
            fabricCanvas.current.add(textObj);
            devLog(`Zone ${index + 1} text created: "${customTextRef.current || zone.placeholder}"`);
          }
          
          // Always show mapping boxes for coordinate reference
          const maxWidthPx = (zone.maxWidth / 1000) * 500;
          const box = new fabric.Rect({
            left, top,
            width: maxWidthPx,
            height: zone.fontSize || 40,
            originX: 'center',
            originY: 'center',
            fill: 'transparent',
            stroke: 'rgba(255, 0, 0, 0.3)',
            strokeDashArray: [5, 5],
            selectable: false,
            evented: false,
            data: { isBoundingBox: true, zoneId: zone.id }
          });
          fabricCanvas.current.add(box);
        }
      });
      
      devLog('All zones initialized, canvas objects:', fabricCanvas.current.getObjects().length);
    };

    // Removed redundant loadBaseImage call here - now called inside initCanvas

    // Responsive scaling with ResizeObserver
    const resizeObserver = new ResizeObserver(entries => {
      for (let entry of entries) {
        if (!fabricCanvas.current) return;
        const { width } = entry.contentRect;
        const height = width; 
        fabricCanvas.current.setDimensions({ width, height });
        fabricCanvas.current.setZoom(width / 500);
        fabricCanvas.current.requestRenderAll();
      }
    });

    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }

    return () => {
      clearTimeout(timer);
      resizeObserver.disconnect();
      if (fabricCanvas.current) {
        devLog('Cleanup - disposing canvas');
        fabricCanvas.current.dispose();
        fabricCanvas.current = null;
      }
    };
  }, [productConfig, isMappingMode]); 

  // Update text or logo dynamically (debounced)
  useEffect(() => {
    if (!fabricCanvas.current || !productConfig || !productConfig.zones) {
      devLog('Skipping text update - canvas or config not ready');
      return;
    }

    const timeoutId = setTimeout(() => {
      try {
        if (!fabricCanvas.current) {
          devError('Canvas disposed during timeout');
          return;
        }

        const objects = fabricCanvas.current.getObjects();
        let hasWarning = false;
      
      productConfig.zones.forEach(zone => {
        const obj = objects.find(o => o.data?.zoneId === zone.id && !o.data?.isBoundingBox);
        if (obj) {
          const textToRender = customText || zone.placeholder;
          let currentFontSize = zone.fontSize || 40;
          let currentCharSpacing = 0; 

          if (zone.isCurved) {
             zone.fontSize = currentFontSize;
             zone.fill = textColor || zone.fill || '#000';
             updateCurvedText(obj, textToRender, zone, textColor);
             
             // Simple auto-fit for curved text group width
             const maxWidthPx = (zone.maxWidth / 1000) * 500;
             if (obj.width * obj.scaleX > maxWidthPx) {
                hasWarning = true;
             }
          } else {
            obj.set({ 
              text: textToRender, 
              fontSize: currentFontSize, 
              charSpacing: currentCharSpacing,
              fill: textColor || zone.fill || '#000'
            });
            
            // Auto-fit Logic
            const maxWidthPx = (zone.maxWidth / 1000) * 500;
            const minFontSize = zone.minFontSize || 12;
            
            while (obj.width * obj.scaleX > maxWidthPx && currentFontSize > minFontSize) {
              currentFontSize -= 2;
              obj.set({ fontSize: currentFontSize });
            }
            
            // If still too wide, try negative char spacing
            while (obj.width * obj.scaleX > maxWidthPx && currentCharSpacing > -100) {
              currentCharSpacing -= 10;
              obj.set({ charSpacing: currentCharSpacing });
            }

            if (obj.width * obj.scaleX > maxWidthPx) {
              hasWarning = true;
            }
          }
        }
      });

      if (hasWarning && onWarning) {
        onWarning(`Name too long (Max fit reached)`);
      } else if (!hasWarning && onWarning) {
        onWarning(''); 
      }

      // Handle Logo
      const updateLogo = async () => {
        const existingLogo = objects.find(o => o.data?.isLogo);
        let currentLeft, currentTop, currentScaleX, currentScaleY;
        
        if (existingLogo) {
          currentLeft = existingLogo.left;
          currentTop = existingLogo.top;
          currentScaleX = existingLogo.scaleX;
          currentScaleY = existingLogo.scaleY;
          fabricCanvas.current.remove(existingLogo);
        }

        if (logoImage) {
          try {
            const img = await fabric.Image.fromURL(logoImage);
            const zone = productConfig.zones[0];
            const left = currentLeft !== undefined ? currentLeft : (zone.x / 1000) * 500;
            const top = currentTop !== undefined ? currentTop : (zone.y / 1000) * 500;
            const maxWidth = (zone.maxWidth / 1000) * 500;
            const logoScale = currentScaleX !== undefined ? currentScaleX : (maxWidth * 0.8) / img.width;
            
            img.set({
              scaleX: logoScale,
              scaleY: currentScaleY !== undefined ? currentScaleY : logoScale,
              left, top,
              originX: 'center', originY: 'center',
              selectable: true,
              evented: true,
              hasControls: true,
              hasBorders: true,
              data: { isLogo: true }
            });
            fabricCanvas.current.add(img);
            
            const textObj = objects.find(o => o.data?.zoneId === zone.id && !o.data?.isBoundingBox);
            if (textObj) textObj.set({ opacity: 0 });
          } catch (err) {
            devError("Error loading logo:", err);
          }
        } else {
          const zone = productConfig.zones[0];
          const textObj = objects.find(o => o.data?.zoneId === zone.id && !o.data?.isBoundingBox);
          if (textObj) textObj.set({ opacity: zone.opacity || 1 });
        }
        fabricCanvas.current.requestRenderAll();
        
        const dataUrl = fabricCanvas.current.toDataURL({ format: 'png', quality: 1, multiplier: 2 });
        onImageExport?.(dataUrl);
      };

      updateLogo();
      } catch (err) {
        devError("Error updating canvas:", err);
      }
    }, 100); // Increased debounce to 100ms for stability 

    return () => clearTimeout(timeoutId);
  }, [customText, textColor, logoImage, productConfig, isMappingMode, onImageExport, onWarning]);

  return (
    <div className="w-full h-full relative group flex flex-col">
      <div ref={containerRef} className="w-full aspect-square bg-gray-50 rounded-2xl overflow-hidden relative shadow-inner">
        {loading && (
          <div className="absolute inset-0 z-10 flex items-center justify-center bg-white/80">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        )}
        <canvas ref={canvasRef} />
        
      <div className="absolute bottom-2 left-2 bg-primary/90 text-white text-[10px] font-bold px-2 py-1 rounded">
        📍 Coordinate Mapping Active
      </div>
      </div>
    </div>
  );
};

export default CanvasCustomizer;

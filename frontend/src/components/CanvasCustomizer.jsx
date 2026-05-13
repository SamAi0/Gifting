import { useEffect, useRef, useState } from 'react';
import * as fabric from 'fabric';

// Development mode logger - only logs in development
// const isDev = import.meta.env.DEV;

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
const CanvasCustomizer = ({ productConfig, textEntries, textColor, logoPreviews, onImageExport, onWarning }) => {
  const canvasRef = useRef(null);
  const fabricCanvas = useRef(null);
  const containerRef = useRef(null);
  const [loading, setLoading] = useState(true);
  const prevProductSlug = useRef(null);

  // Helper for curved text
  const updateCurvedText = (group, text, zone, currentTextColor) => {
    if (!group || !fabricCanvas.current) return;
    
    group.clear();
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
    if (!canvasRef.current || !productConfig || !productConfig.baseImage) return;

    const productSlug = productConfig.baseImage;
    const zonesKey = JSON.stringify(productConfig.zones);
    if (prevProductSlug.current === `${productSlug}-${zonesKey}` && fabricCanvas.current) return;
    prevProductSlug.current = `${productSlug}-${zonesKey}`;

    if (fabricCanvas.current) {
      fabricCanvas.current.dispose();
      fabricCanvas.current = null;
    }

    let initTimer;

    const initCanvas = async () => {
      // Safety check: Don't initialize if already initialized or if ref is lost
      if (!canvasRef.current || fabricCanvas.current) return;

      try {
        fabricCanvas.current = new fabric.Canvas(canvasRef.current, {
          width: 500,
          height: 500,
          backgroundColor: '#f3f4f6',
          selection: true,
        });

        fabricCanvas.current.on('object:modified', (e) => {
          logCoordinates(e.target);
          if (!fabricCanvas.current) return;
          fabricCanvas.current.requestRenderAll();
          const dataUrl = fabricCanvas.current.toDataURL({ format: 'png', quality: 1, multiplier: 2 });
          onImageExport?.(dataUrl);
        });
        // fabricCanvas.current.on('object:moving', (e) => logCoordinates(e.target));
        // fabricCanvas.current.on('object:rotating', (e) => logCoordinates(e.target));

        console.log("%c Customizer Engine Ready ", "background: #2ecc71; color: white; font-weight: bold;");

        const logCoordinates = (obj) => {
          if (!fabricCanvas.current || !obj || !obj.data?.zoneId) return;
          
          const canvasWidth = fabricCanvas.current.width;
          const canvasHeight = fabricCanvas.current.height;
          
          const x = Math.round((obj.left / canvasWidth) * 1000);
          const y = Math.round((obj.top / canvasHeight) * 1000);
          const angle = Math.round(obj.angle || 0);
          
          // console.clear(); // Removed to keep other debug logs visible
          console.log(`%c Zone Update [${obj.data.zoneId}] `, 'background: #D91656; color: white; font-weight: bold;');
          console.log(`"x": ${x}, "y": ${y}, "angle": ${angle}`);
          console.log(`--------------------------`);
        };

        await loadBaseImage();
      } catch (error) {
        console.error('Failed to initialize canvas:', error);
      }
    };

    const loadBaseImage = async () => {
      try {
        setLoading(true);
        const img = await fabric.Image.fromURL(productConfig.baseImage, { crossOrigin: 'anonymous' });
        if (!fabricCanvas.current) return;
        
        const canvasWidth = 500;
        const scale = Math.min(canvasWidth / img.width, canvasWidth / img.height) * 0.98; 
        
        img.set({
          scaleX: scale, scaleY: scale,
          left: 250, top: 250,
          originX: 'center', originY: 'center',
          selectable: false, evented: true,
          data: { isBaseImage: true }
        });

        fabricCanvas.current.add(img);
        initZones();
        fabricCanvas.current.requestRenderAll();
      } catch (err) {
        console.error("Failed to load base image:", err);
      } finally {
        if (fabricCanvas.current) setLoading(false);
      }
    };

    const initZones = () => {
      if (!fabricCanvas.current) return;
      productConfig.zones.forEach((zone) => {
        const left = (zone.x / 1000) * 500;
        const top = (zone.y / 1000) * 500;
        
        const maxWidthPx = (zone.maxWidth / 1000) * 500 || (zone.width / 1000) * 500 || 100;
        const box = new fabric.Rect({
          left, top,
          width: maxWidthPx,
          height: zone.fontSize || (zone.height / 1000) * 500 || 40,
          originX: 'center', originY: 'center',
          fill: 'transparent',
          stroke: 'rgba(217, 22, 86, 0.5)',
          strokeDashArray: [5, 5],
          selectable: false, evented: false,
          data: { isBoundingBox: true, zoneId: zone.id }
        });
        fabricCanvas.current.add(box);
      });
    };

    initTimer = setTimeout(initCanvas, 100);

    const resizeObserver = new ResizeObserver(entries => {
      for (let entry of entries) {
        if (!fabricCanvas.current) return;
        const { width } = entry.contentRect;
        fabricCanvas.current.setDimensions({ width, height: width });
        fabricCanvas.current.setZoom(width / 500);
        fabricCanvas.current.requestRenderAll();
      }
    });

    if (containerRef.current) resizeObserver.observe(containerRef.current);

    return () => {
      if (initTimer) clearTimeout(initTimer);
      resizeObserver.disconnect();
      if (fabricCanvas.current) {
        fabricCanvas.current.dispose();
        fabricCanvas.current = null;
      }
    };
  }, [productConfig, onImageExport]); 

  // Dynamic Updates (Grouped Mapping Mode)
  useEffect(() => {
    if (!fabricCanvas.current || !productConfig || !textEntries) return;

    const timeoutId = setTimeout(async () => {
      try {
        const objects = fabricCanvas.current.getObjects();
        let hasWarning = false;

        const totalZones = productConfig.zones.length;

        for (let i = 0; i < totalZones; i++) {
          const zone = productConfig.zones[i];
          let obj = objects.find(o => o.data?.zoneId === zone.id && !o.data?.isBoundingBox);
          const left = (zone.x / 1000) * 500;
          const top = (zone.y / 1000) * 500;

          // TWO-WAY MAPPING LOGIC
          let targetType = zone.type || 'text';
          let targetValue = null;

          if (targetType === 'text') {
            // If we have a text entry for this index, use it. 
            // Otherwise, targetValue remains null which triggers placeholder.
            if (i < textEntries.length) {
              targetValue = textEntries[i].text;
            }
          } else if (targetType === 'image') {
            // Logo fills from the end of the image-type zones if possible
            // Simplified: if it's an image zone, try to find a logo
            if (logoPreviews && logoPreviews.length > 0) {
                // Find which image zone this is (0th image zone gets 0th logo)
                const imageZones = productConfig.zones.filter(z => z.type === 'image');
                const imgZoneIdx = imageZones.findIndex(z => z.id === zone.id);
                if (imgZoneIdx !== -1 && imgZoneIdx < logoPreviews.length) {
                    targetValue = logoPreviews[imgZoneIdx];
                }
            }
          }

          // Clean up if type changed or no targetType
          const isTextType = obj?.type === 'text' || obj?.type === 'group';
          const isImageType = obj?.type === 'image';
          
          if (obj && (
            (targetType === 'text' && !isTextType) || 
            (targetType === 'image' && !isImageType) || 
            !targetType
          )) {
            fabricCanvas.current.remove(obj);
            obj = null;
          }

          if (targetType === 'text') {
            const textToRender = targetValue || zone.placeholder || 'Type...';
            if (!obj) {
              if (zone.isCurved) {
                obj = new fabric.Group([], {
                  left, top,
                  originX: zone.originX || 'center',
                  originY: zone.originY || 'center',
                  angle: zone.angle || 0,
                  selectable: true,
                  data: { zoneId: zone.id, isCurved: true }
                });
              } else {
                obj = new fabric.Text(textToRender, {
                  left, top,
                  originX: zone.originX || 'center',
                  originY: zone.originY || 'center',
                  angle: zone.angle || 0,
                  fontFamily: zone.fontFamily || 'serif',
                  fontSize: zone.fontSize || 40,
                  textAlign: 'center',
                  fill: textColor,
                  selectable: true,
                  data: { zoneId: zone.id }
                });
              }
              fabricCanvas.current.add(obj);
            }

            if (zone.isCurved) {
              updateCurvedText(obj, textToRender, zone, textColor);
            } else {
              obj.set({ text: textToRender, fill: textColor });
              const maxWidthPx = (zone.maxWidth / 1000) * 500;
              let currentFontSize = zone.fontSize || 40;
              const minSize = zone.minFontSize || 10;
              while (obj.width * obj.scaleX > maxWidthPx && currentFontSize > minSize) {
                currentFontSize -= 2;
                obj.set({ fontSize: currentFontSize });
              }
              if (obj.width * obj.scaleX > maxWidthPx) hasWarning = true;
            }
          } else if (targetType === 'image' && targetValue) {
            // Check if image object already exists but has a different source
            if (obj && obj.type === 'image' && obj.data?.src !== targetValue) {
              fabricCanvas.current.remove(obj);
              obj = null;
            }

            if (!obj) {
              try {
                const img = await fabric.Image.fromURL(targetValue, { crossOrigin: 'anonymous' });
                const maxWidth = (zone.maxWidth / 1000) * 500 || (zone.width / 1000) * 500 || 100;
                const maxHeight = (zone.height / 1000) * 500 || 100;
                const scale = Math.min(maxWidth / img.width, maxHeight / img.height) * 0.9;
                
                img.set({
                  left, top,
                  scaleX: scale, scaleY: scale,
                  originX: zone.originX || 'center',
                  originY: zone.originY || 'center',
                  angle: zone.angle || 0,
                  selectable: true, evented: true,
                  data: { zoneId: zone.id, isLogo: true, src: targetValue }
                });
                fabricCanvas.current.add(img);
                obj = img;
              } catch (err) {
                console.error("Error loading image in zone:", err);
              }
            }
          }
        }

        onWarning?.(hasWarning ? "Text too long" : "");
        fabricCanvas.current.requestRenderAll();
        
        const dataUrl = fabricCanvas.current.toDataURL({ format: 'png', quality: 1, multiplier: 2 });
        onImageExport?.(dataUrl);
      } catch (err) {
        console.error("Error updating canvas:", err);
      }
    }, 100);

    return () => clearTimeout(timeoutId);
  }, [textEntries, logoPreviews, textColor, productConfig, onImageExport, onWarning]);

  return (
    <div className="w-full h-full relative group flex flex-col">
      <div ref={containerRef} className="w-full aspect-square bg-gray-50 rounded-2xl overflow-hidden relative shadow-inner">
        {/* Stable wrapper for Fabric.js to prevent React DOM reconciliation errors */}
        <div className="canvas-container-wrapper">
          <canvas ref={canvasRef} />
        </div>
        
        {loading && (
          <div className="absolute inset-0 z-10 flex items-center justify-center bg-white/80">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CanvasCustomizer;

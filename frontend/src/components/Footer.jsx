import { Link } from 'react-router-dom';
import { Gift, Mail, Phone, MapPin, ArrowUpRight } from 'lucide-react';

const FacebookIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
);
const InstagramIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
);
const LinkedinIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
);
const TwitterIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"/></svg>
);

const Footer = () => {
  return (
    <footer className="bg-slate-900 text-white pt-10 pb-6 overflow-hidden relative border-t border-white/5">
      <div className="container-custom relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 mb-8">
          {/* Company Info */}
          <div className="space-y-4">
            <Link to="/" className="flex items-center space-x-3 group">
              <div className="bg-primary p-1.5 rounded-lg shadow-lg shadow-primary/20 transition-transform group-hover:rotate-12">
                <Gift className="text-white w-5 h-5" />
              </div>
              <span className="text-xl font-bold tracking-tight">Soham <span className="text-primary">Gift</span></span>
            </Link>
            <p className="text-slate-400 leading-relaxed font-light text-sm max-w-xs">
              Elevating corporate gifting with personalized, premium solutions that leave a lasting impression.
            </p>
            <div className="flex gap-3">
              {[InstagramIcon, LinkedinIcon, FacebookIcon, TwitterIcon].map((Icon, idx) => (
                <a key={idx} href="#" className="w-9 h-9 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center hover:bg-primary transition-all duration-300 group">
                  <Icon className="w-4 h-4 text-slate-400 group-hover:text-white" />
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-white font-bold mb-4 uppercase tracking-widest text-xs">Explore</h4>
            <ul className="space-y-2">
              {[
                { name: 'Home', path: '/' },
                { name: 'Our Catalog', path: '/products' },
                { name: 'Bulk Inquiry', path: '/bulk-inquiry' },
                { name: 'Our Story', path: '/about' },
                { name: 'Contact Support', path: '/contact' },
              ].map((link) => (
                <li key={link.path}>
                  <Link to={link.path} className="text-slate-400 hover:text-white transition-colors flex items-center gap-2 group text-sm font-medium">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary/40 group-hover:bg-primary transition-colors"></span>
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Collections */}
          <div>
            <h4 className="text-white font-bold mb-4 uppercase tracking-widest text-xs">Collections</h4>
            <ul className="space-y-2">
              {[
                { name: 'Gourmet Hampers', id: '1' },
                { name: 'Office Gifts', id: '2' },
                { name: 'Next-Gen Tech', id: '4' },
                { name: 'Signature Sets', id: '7' },
              ].map((cat) => (
                <li key={cat.id}>
                  <Link to={`/products?category=${cat.id}`} className="text-slate-400 hover:text-white transition-colors flex items-center justify-between group text-sm font-medium">
                    {cat.name}
                    <ArrowUpRight size={14} className="opacity-0 group-hover:opacity-100 transition-all -translate-x-1 group-hover:translate-x-0" />
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-white font-bold mb-4 uppercase tracking-widest text-xs">Get In Touch</h4>
            <ul className="space-y-3">
              <li className="flex items-start gap-2">
                <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center text-primary flex-shrink-0 border border-white/5">
                  <MapPin size={16} />
                </div>
                <span className="text-slate-400 text-sm leading-relaxed">Airoli, Navi Mumbai, India</span>
              </li>
              <li className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center text-primary flex-shrink-0 border border-white/5">
                  <Phone size={16} />
                </div>
                <span className="text-slate-400 text-sm font-bold">+91 81699 75287</span>
              </li>
              <li className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center text-primary flex-shrink-0 border border-white/5">
                  <Mail size={16} />
                </div>
                <span className="text-slate-400 text-sm font-medium">corporate@sohamgift.com</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-6 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-slate-500 text-sm">
            © {new Date().getFullYear()} <span className="text-white font-bold">Soham Gift</span>. India.
          </p>
          <div className="flex gap-10">
            <Link to="/privacy" className="text-slate-500 hover:text-white text-xs font-bold transition-colors">Privacy Policy</Link>
            <Link to="/terms" className="text-slate-500 hover:text-white text-xs font-bold transition-colors">Terms of Service</Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

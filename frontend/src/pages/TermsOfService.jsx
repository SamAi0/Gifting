import { Helmet } from 'react-helmet-async';

const TermsOfService = () => {
  return (
    <div className="pt-32 pb-20 bg-slate-50 min-h-screen">
      <Helmet>
        <title>Terms of Service | Soham Gift</title>
        <meta name="description" content="Terms of Service for Soham Gift. Please read our terms and conditions carefully." />
      </Helmet>
      
      <div className="container-custom max-w-4xl">
        <div className="bg-white rounded-3xl p-8 md:p-12 shadow-sm border border-slate-100">
          <h1 className="text-3xl md:text-4xl font-bold text-slate-900 mb-2">Terms of Service</h1>
          <p className="text-slate-500 mb-8">Last updated: {new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</p>
          
          <div className="prose prose-slate max-w-none prose-headings:text-slate-900 prose-p:text-slate-600 prose-li:text-slate-600">
            <h2 className="text-xl font-bold mt-8 mb-4">1. Agreement to Terms</h2>
            <p className="mb-4">
              By accessing our website and purchasing our products, you agree to be bound by these Terms of Service. If you do not agree with any part of these terms, please do not use our services.
            </p>

            <h2 className="text-xl font-bold mt-8 mb-4">2. Products and Customization</h2>
            <p className="mb-4">
              We specialize in corporate gifting and custom products. Please note:
            </p>
            <ul className="list-disc pl-6 mb-4 space-y-2">
              <li>By uploading a logo or artwork for customization, you warrant that you hold the necessary copyrights or permissions to use such materials.</li>
              <li>Soham Gift is not liable for any copyright infringement resulting from customer-supplied artwork.</li>
              <li>Product colors, textures, and print results may vary slightly from digital mockups.</li>
            </ul>

            <h2 className="text-xl font-bold mt-8 mb-4">3. Ordering and Payment</h2>
            <p className="mb-4">
              All orders are subject to acceptance and availability. Prices for our products are subject to change without notice. We reserve the right to refuse any order you place with us.
            </p>

            <h2 className="text-xl font-bold mt-8 mb-4">4. Shipping and Delivery</h2>
            <p className="mb-4">
              We aim to deliver products within the estimated timeframes; however, delays are occasionally inevitable due to unforeseen factors. We shall be under no liability for any delay or failure to deliver the products within estimated timescales.
            </p>

            <h2 className="text-xl font-bold mt-8 mb-4">5. Cancellations, Returns, and Refunds</h2>
            <p className="mb-4">
              Our policy on returns and cancellations is as follows:
            </p>
            <ul className="list-disc pl-6 mb-4 space-y-2">
              <li><strong>Customized Products:</strong> Orders for customized products cannot be cancelled once production has commenced. We do not accept returns for customized items unless they arrive damaged or defective.</li>
              <li><strong>Damaged/Defective Items:</strong> You must notify us within 48 hours of delivery if an item is damaged. We will arrange a replacement or refund upon verification.</li>
              <li><strong>Refund Processing:</strong> Approved refunds will be processed within 5-7 business days back to the original payment method.</li>
            </ul>

            <h2 className="text-xl font-bold mt-8 mb-4">6. Changes to Terms of Service</h2>
            <p className="mb-4">
              We reserve the right, at our sole discretion, to update, change or replace any part of these Terms of Service by posting updates and changes to our website. It is your responsibility to check our website periodically for changes.
            </p>
            
            <h2 className="text-xl font-bold mt-8 mb-4">7. Contact Information</h2>
            <p className="mb-4">
              Questions about the Terms of Service should be sent to us via our Contact Us page.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TermsOfService;

import { Helmet } from 'react-helmet-async';
import BulkOrderForm from '../components/BulkOrderForm';

const BulkOrders = () => {
  return (
    <div className="pt-24 bg-slate-50 min-h-screen">
      <Helmet>
        <title>Bulk Orders & Corporate Gifting | Soham Gift</title>
        <meta name="description" content="Contact us for bulk corporate gifting solutions. We offer tailored gifts and special pricing for Corporates, Event Planners, and Retail Stores." />
      </Helmet>
      
      <div className="container-custom pb-8">
        <div className="text-center mb-4">
           <h1 className="text-3xl font-bold text-slate-900">Partner With Us</h1>
           <p className="text-slate-500 mt-2">Scale your gifting effortlessly.</p>
        </div>
      </div>
      
      <BulkOrderForm />
    </div>
  );
};

export default BulkOrders;

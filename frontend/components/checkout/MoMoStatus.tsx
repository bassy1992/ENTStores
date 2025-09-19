import { useEffect, useState } from 'react';
import { Card, CardContent } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { CheckCircle, Clock, AlertCircle, Smartphone, RefreshCw } from 'lucide-react';

interface MoMoStatusProps {
  reference: string;
  onSuccess: (transactionId: string) => void;
  onFailure: (reason: string) => void;
}

interface MoMoTransaction {
  reference: string;
  status: 'pending' | 'processing' | 'success' | 'failed';
  phone: string;
  amount: number;
  currency: string;
  message?: string;
  failureReason?: string;
  transactionId?: string;
}

export function MoMoStatus({ reference, onSuccess, onFailure }: MoMoStatusProps) {
  const [transaction, setTransaction] = useState<MoMoTransaction | null>(null);
  const [isPolling, setIsPolling] = useState(true);

  useEffect(() => {
    if (!reference || !isPolling) return;

    const pollStatus = async () => {
      try {
        const response = await fetch(`/api/momo/status/${reference}`);
        const data = await response.json();
        
        setTransaction(data);

        if (data.status === 'success') {
          setIsPolling(false);
          onSuccess(data.transactionId || reference);
        } else if (data.status === 'failed') {
          setIsPolling(false);
          onFailure(data.failureReason || 'Payment failed');
        }
      } catch (error) {
        console.error('Error polling MoMo status:', error);
      }
    };

    // Poll immediately, then every 3 seconds
    pollStatus();
    const interval = setInterval(pollStatus, 3000);

    // Stop polling after 5 minutes
    const timeout = setTimeout(() => {
      setIsPolling(false);
      clearInterval(interval);
    }, 300000);

    return () => {
      clearInterval(interval);
      clearTimeout(timeout);
    };
  }, [reference, isPolling, onSuccess, onFailure]);

  if (!transaction) {
    return (
      <Card className="border-blue-200 bg-blue-50">
        <CardContent className="p-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
            <div>
              <div className="font-medium text-blue-900">Initializing Payment...</div>
              <div className="text-sm text-blue-700">Setting up your MTN MoMo payment</div>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  const getStatusIcon = () => {
    switch (transaction.status) {
      case 'pending':
        return <Clock className="w-5 h-5 text-yellow-600" />;
      case 'processing':
        return <RefreshCw className="w-5 h-5 text-blue-600 animate-spin" />;
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'failed':
        return <AlertCircle className="w-5 h-5 text-red-600" />;
      default:
        return <Clock className="w-5 h-5 text-gray-600" />;
    }
  };

  const getStatusColor = () => {
    switch (transaction.status) {
      case 'pending':
        return 'border-yellow-200 bg-yellow-50';
      case 'processing':
        return 'border-blue-200 bg-blue-50';
      case 'success':
        return 'border-green-200 bg-green-50';
      case 'failed':
        return 'border-red-200 bg-red-50';
      default:
        return 'border-gray-200 bg-gray-50';
    }
  };

  const getStatusBadge = () => {
    switch (transaction.status) {
      case 'pending':
        return <Badge variant="outline" className="bg-yellow-100 text-yellow-700 border-yellow-300">Pending</Badge>;
      case 'processing':
        return <Badge variant="outline" className="bg-blue-100 text-blue-700 border-blue-300">Processing</Badge>;
      case 'success':
        return <Badge variant="outline" className="bg-green-100 text-green-700 border-green-300">Success</Badge>;
      case 'failed':
        return <Badge variant="outline" className="bg-red-100 text-red-700 border-red-300">Failed</Badge>;
      default:
        return <Badge variant="outline">Unknown</Badge>;
    }
  };

  return (
    <Card className={getStatusColor()}>
      <CardContent className="p-4 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {getStatusIcon()}
            <div>
              <div className="font-medium">MTN MoMo Payment</div>
              <div className="text-sm text-gray-600">
                {transaction.currency} {transaction.amount} to {transaction.phone}
              </div>
            </div>
          </div>
          {getStatusBadge()}
        </div>

        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600">Reference:</span>
            <span className="font-mono font-medium">{transaction.reference}</span>
          </div>
          {transaction.transactionId && (
            <div className="flex justify-between">
              <span className="text-gray-600">Transaction ID:</span>
              <span className="font-mono font-medium">{transaction.transactionId}</span>
            </div>
          )}
        </div>

        {transaction.message && (
          <div className="p-3 rounded-lg bg-white/50 border">
            <div className="flex items-start gap-2">
              <Smartphone className="w-4 h-4 mt-0.5 text-gray-500" />
              <div className="text-sm text-gray-700">{transaction.message}</div>
            </div>
          </div>
        )}

        {transaction.status === 'pending' && (
          <div className="p-3 rounded-lg bg-white/50 border">
            <div className="text-sm text-gray-700">
              <strong>Next steps:</strong>
              <ul className="mt-1 space-y-1 text-xs">
                <li>• Check your phone for MTN MoMo authorization prompt</li>
                <li>• Or dial *170# and follow the prompts</li>
                <li>• Enter your MoMo PIN to complete payment</li>
              </ul>
            </div>
          </div>
        )}

        {transaction.status === 'failed' && transaction.failureReason && (
          <div className="p-3 rounded-lg bg-red-50 border border-red-200">
            <div className="text-sm text-red-700">
              <strong>Payment Failed:</strong> {transaction.failureReason}
            </div>
          </div>
        )}

        {(transaction.status === 'pending' || transaction.status === 'processing') && (
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
            <span>Checking payment status automatically...</span>
          </div>
        )}

        {transaction.status === 'failed' && (
          <Button 
            variant="outline" 
            size="sm" 
            onClick={() => window.location.reload()}
            className="w-full"
          >
            Try Again
          </Button>
        )}
      </CardContent>
    </Card>
  );
}
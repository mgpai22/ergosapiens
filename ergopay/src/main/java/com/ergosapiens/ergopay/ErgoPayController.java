package com.ergosapiens.ergopay;

import org.ergoplatform.P2PKAddress;
import org.ergoplatform.appkit.*;
import org.ergoplatform.appkit.impl.ErgoTreeContract;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.Collections;
import java.util.List;
import java.util.function.Function;

import static org.ergoplatform.appkit.Parameters.MinFee;

@RestController
public class ErgoPayController {

    private ReducedTransaction getReducedTx(boolean isMainNet, long amountToSpend, List<ErgoToken> tokensToSpend,
                                            Address sender,
                                            Function<UnsignedTransactionBuilder, UnsignedTransactionBuilder> outputBuilder) {
        NetworkType networkType = isMainNet ? NetworkType.MAINNET : NetworkType.TESTNET;
        return RestApiErgoClient.create(
                getDefaultNodeUrl(isMainNet),
                networkType,
                "",
                RestApiErgoClient.getDefaultExplorerUrl(networkType)
        ).execute(ctx -> {

            List<InputBox> boxesToSpend = BoxOperations.createForSender(sender, ctx)
                    .withAmountToSpend(amountToSpend)
                    .withTokensToSpend(tokensToSpend)
                    .loadTop();

            P2PKAddress changeAddress = sender.asP2PK();
            UnsignedTransactionBuilder txB = ctx.newTxBuilder();

            UnsignedTransactionBuilder unsignedTransactionBuilder = txB.boxesToSpend(boxesToSpend)
                    .fee(MinFee)
                    .sendChangeTo(changeAddress);

            UnsignedTransaction unsignedTransaction = outputBuilder.apply(unsignedTransactionBuilder).build();

            return ctx.newProverBuilder().build().reduce(unsignedTransaction, 0);
        });
    }


    @GetMapping("/ergopay/demo/{recipientAddress}/{address}/{amountERG}/{ref}")
    public ErgoPayResponse mintTokenDemo(@PathVariable String address, @PathVariable String recipientAddress,@PathVariable double amountERG, @PathVariable String ref) {

        ErgoPayResponse response = new ErgoPayResponse();
        long nanoERGs = (long)Math.pow(10, 9);


        try {
            boolean isMainNet = isMainNetAddress(address);
            long amountToSend = (long)(amountERG * nanoERGs);
            Address sender = Address.create(address);
            Address recipient = Address.create(recipientAddress);
            String paymentPortalIdentifier = "Ergo Payment Portal";
            ErgoValue encodedRef = ErgoValue.of(ref.getBytes(StandardCharsets.UTF_8));
            ErgoValue EncodedPaymentPortalIdentifier = ErgoValue.of(paymentPortalIdentifier.getBytes(StandardCharsets.UTF_8));


            byte[] reduced = getReducedTx(isMainNet, amountToSend, Collections.emptyList(), sender,
                    unsignedTxBuilder -> {
                        NetworkType networkType = isMainNet ? NetworkType.MAINNET : NetworkType.TESTNET;

                        ErgoTreeContract contract = new ErgoTreeContract(recipient.getErgoAddress().script(), networkType);

                        OutBoxBuilder outBoxBuilder = unsignedTxBuilder.outBoxBuilder()
                                .value(amountToSend)
                                .contract(contract)
                                .registers(encodedRef, EncodedPaymentPortalIdentifier);

                        OutBox newBox = outBoxBuilder.build();

                        unsignedTxBuilder.outputs(newBox);

                        return unsignedTxBuilder;
                    }
            ).toBytes();

            response.reducedTx = Base64.getUrlEncoder().encodeToString(reduced);
            response.address = address;
            response.message = "Do not send. Your payment identifier is: " + ref;
            response.messageSeverity = ErgoPayResponse.Severity.INFORMATION;

        } catch (Throwable t) {
            response.messageSeverity = ErgoPayResponse.Severity.ERROR;
            response.message = (t.getMessage());
        }

        return response;
    }

    @GetMapping("/ergopay/{recipientAddress}/{address}/{amountERG}/{ref}")
    public ErgoPayResponse mintToken(@PathVariable String address, @PathVariable String recipientAddress,@PathVariable double amountERG, @PathVariable String ref) {

        ErgoPayResponse response = new ErgoPayResponse();
        long nanoERGs = (long)Math.pow(10, 9);


        try {
            boolean isMainNet = isMainNetAddress(address);
            long amountToSend = (long)(amountERG * nanoERGs);
            Address sender = Address.create(address);
            Address recipient = Address.create(recipientAddress);
            String paymentPortalIdentifier = "Ergo Payment Portal";
            ErgoValue encodedRef = ErgoValue.of(ref.getBytes(StandardCharsets.UTF_8));
            ErgoValue EncodedPaymentPortalIdentifier = ErgoValue.of(paymentPortalIdentifier.getBytes(StandardCharsets.UTF_8));


            byte[] reduced = getReducedTx(isMainNet, amountToSend, Collections.emptyList(), sender,
                    unsignedTxBuilder -> {

                        NetworkType networkType = isMainNet ? NetworkType.MAINNET : NetworkType.TESTNET;


                        ErgoTreeContract contract = new ErgoTreeContract(recipient.getErgoAddress().script(), networkType);

                        OutBoxBuilder outBoxBuilder = unsignedTxBuilder.outBoxBuilder()
                                .value(amountToSend)
                                .contract(contract)
                                .registers(encodedRef, EncodedPaymentPortalIdentifier);

                        OutBox newBox = outBoxBuilder.build();

                        unsignedTxBuilder.outputs(newBox);

                        return unsignedTxBuilder;
                    }
            ).toBytes();

            response.reducedTx = Base64.getUrlEncoder().encodeToString(reduced);
            response.address = address;
            response.message = "Your payment identifier is: " + ref + ". Make sure to save it!";
            response.messageSeverity = ErgoPayResponse.Severity.INFORMATION;

        } catch (Throwable t) {
            response.messageSeverity = ErgoPayResponse.Severity.ERROR;
            response.message = (t.getMessage());
        }

        return response;
    }

    private static boolean isMainNetAddress(String address) {
        try {
            return Address.create(address).isMainnet();
        } catch (Throwable t) {
            throw new IllegalArgumentException("Invalid address: " + address);
        }
    }
    private static String getDefaultNodeUrl(boolean mainNet) {
        return mainNet ? NODE_MAINNET : NODE_TESTNET;
    }

    public static final String NODE_MAINNET = "http://213.239.193.208:9053/";
    public static final String NODE_TESTNET = "http://213.239.193.208:9052/";
}
